from bs4 import BeautifulSoup
import urllib.parse

def GetExternalHyperlinkRatio(html_content, base_url):
    """
    Tính tỷ lệ liên kết NGOẠI VI (external hyperlinks) trong HTML.
    
    Args:
        html_content (str): Nội dung HTML
        base_url (str): URL gốc để chuẩn hóa liên kết (ví dụ: https://example.com)
    
    Returns:
        float: Tỷ lệ external links (0.0 đến 1.0)
    """
    try:
        # Phân tích HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Lấy domain gốc
        parsed_base = urllib.parse.urlparse(base_url)
        base_domain = parsed_base.netloc.lower()
        if base_domain.startswith('www.'):
            base_domain = base_domain[4:]  # Bỏ www. để so sánh chính xác hơn
        
        # Tìm tất cả thẻ <a> có href
        hyperlinks = soup.find_all('a', href=True)
        
        if not hyperlinks:
            return 0.0
        
        valid_links = 0
        external_links = 0
        
        for link in hyperlinks:
            href = link['href'].strip()
            
            # Bỏ qua liên kết không hợp lệ
            if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue
                
            # Chuẩn hóa URL tuyệt đối
            absolute_url = urllib.parse.urljoin(base_url, href)
            parsed_href = urllib.parse.urlparse(absolute_url)
            href_domain = parsed_href.netloc.lower()
            
            # Bỏ www. để so sánh công bằng
            if href_domain.startswith('www.'):
                href_domain = href_domain[4:]
            
            valid_links += 1
            
            # Nếu KHÔNG cùng domain → là external
            if href_domain and href_domain != base_domain:
                external_links += 1
        
        # Tính tỷ lệ external
        ratio = external_links / valid_links if valid_links > 0 else 0.0
        return round(ratio, 4)
    
    except Exception as e:
        print(f"[Lỗi GetExternalHyperlinkRatio]: {e}")
        return 0.0


# === VÍ DỤ SỬ DỤNG ===
if __name__ == "__main__":
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <a href="/about">Internal 1</a>
        <a href="https://example.com/contact">Internal 2</a>
        <a href="https://google.com">External 1</a>
        <a href="http://facebook.com">External 2</a>
        <a href="javascript:alert(1)">Invalid</a>
        <a href="#top">Anchor</a>
        <a href="/blog/post1.html">Internal 3</a>
    </body>
    </html>
    """
    
    base_url = "https://example.com"
    ratio = GetExternalHyperlinkRatio(sample_html, base_url)
    print(f"Tỷ lệ external hyperlinks: {ratio:.4f}")
    # Kết quả mong đợi: 2 external / 4 valid = 0.5000
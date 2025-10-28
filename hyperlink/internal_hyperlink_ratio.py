from bs4 import BeautifulSoup
import urllib.parse
import re

def GetInternalHyperlinkRatio(html_content, base_url):
    try:
        # Tạo đối tượng BeautifulSoup để phân tích HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Lấy domain từ base_url
        parsed_url = urllib.parse.urlparse(base_url)
        base_domain = parsed_url.netloc.lower()  # Lấy domain (ví dụ: example.com)
        
        # Tìm tất cả các thẻ <a> có thuộc tính href
        hyperlinks = soup.find_all('a', href=True)
        
        if not hyperlinks:
            return 0.0  # Không có hyperlink, trả về 0.0
        
        total_links = len(hyperlinks)
        internal_links = 0
        
        # Duyệt qua từng liên kết để kiểm tra internal/external
        for link in hyperlinks:
            href = link['href'].strip()

            if not href or href.startswith('#'):
                total_links -= 1
                continue
            
            # Bỏ qua các liên kết rỗng hoặc không hợp lệ
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
                
            # Chuẩn hóa URL
            absolute_url = urllib.parse.urljoin(base_url, href)
            parsed_href = urllib.parse.urlparse(absolute_url)
            href_domain = parsed_href.netloc.lower()
            
            # Kiểm tra nếu domain của liên kết khớp với base_domain
            if href_domain == base_domain or not href_domain:  # Không domain = internal (liên kết tương đối)
                internal_links += 1
        
        # Tính tỷ lệ
        ratio = internal_links / total_links if total_links > 0 else 0.0
        return ratio
    
    except Exception as e:
        print(f"Lỗi khi xử lý HTML: {str(e)}")
        return 0.0

# Ví dụ sử dụng
if __name__ == "__main__":
    # Ví dụ HTML mẫu
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <a href="/page1">Internal Link 1</a>
        <a href="https://example.com/page2">Internal Link 2</a>
        <a href="https://other.com/page3">External Link</a>
        <a href="javascript:void(0)">Invalid Link</a>
        <a href="#section1">Anchor Link</a>
    </body>
    </html>
    """
    
    base_url = "https://example.com"
    ratio = GetInternalHyperlinkRatio(sample_html, base_url)
    print(f"Tỷ lệ internal hyperlinks: {ratio:.2f}")
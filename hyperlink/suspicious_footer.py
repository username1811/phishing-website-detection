from bs4 import BeautifulSoup

def calculate_footer_common_link_ratio(html_content):
    """
    Tính tỷ lệ tần suất liên kết phổ biến nhất trong footer so với tổng số liên kết anchor trong footer.
    
    Args:
        html_content (str): Nội dung HTML của trang web.
    
    Returns:
        float: Tỷ lệ HF9 (0 nếu không có anchor link trong footer, hoặc giá trị từ 0 đến 1 nếu có).
    """
    try:
        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Tìm phần footer (giả định có thẻ <footer> hoặc class/id như 'footer')
        footer = soup.find('footer')
        if not footer:
            return 0  # Không có footer, coi là 0
        
        # Tìm tất cả các thẻ <a> trong footer có thuộc tính href
        anchors = footer.find_all('a', href=True)
        if not anchors:
            return 0  # Không có anchor link trong footer, coi là 0
        
        # Lấy danh sách href và đếm tần suất
        hrefs = [a['href'].lower() for a in anchors]
        if not hrefs:
            return 0
        
        # Tìm tần suất của liên kết phổ biến nhất
        freq_most_common = max(set(hrefs), key=hrefs.count, default=0)
        if not freq_most_common:
            return 0
        
        freq = hrefs.count(freq_most_common)
        total_anchors = len(hrefs)
        
        # Tính tỷ lệ
        ratio = freq / total_anchors if total_anchors > 0 else 0
        return ratio
        
    except Exception as e:
        print(f"Lỗi khi xử lý HTML: {str(e)}")
        return 0  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Ví dụ HTML mẫu (tính đến 02:54 PM +07, Chủ nhật, 26/10/2025)
    html_samples = [
        """
        <html><body>
            <footer>
                <a href="/login"></a><a href="/login"></a><a href="/contact"></a>
            </footer>
        </body></html>
        """,  # Tỷ lệ: 2/3 ≈ 0.667
        """
        <html><body>
            <footer>
                <a href="/about"></a><a href="/contact"></a><a href="/privacy"></a>
            </footer>
        </body></html>
        """,  # Tỷ lệ: 1/3 ≈ 0.333
        """
        <html><body>
            <footer></footer>
        </body></html>
        """,  # Tỷ lệ: 0 (không có anchor)
        """
        <html><body>
            <div>No footer here</div>
        </body></html>
        """,  # Tỷ lệ: 0 (không có footer)
    ]
    
    for i, html in enumerate(html_samples, 1):
        print(f"HTML Sample {i}:")
        print(f"HTML Sample {html}:")
        hf9_value = calculate_footer_common_link_ratio(html)
        print(f"HF9: {hf9_value:.3f} (Tỷ lệ liên kết phổ biến nhất trong footer)")
        print()
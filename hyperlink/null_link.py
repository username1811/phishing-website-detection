from bs4 import BeautifulSoup


def null_link_ratio(html_content):
    """
    Kiểm tra tỷ lệ null anchor link so với tổng anchor link.
    
    Args:
        html_content (str): Nội dung HTML của trang web.
    
    Returns:
        bool: True nếu tỷ lệ null anchor link > 0.34 (HF6 = 1), False nếu không (HF6 = 0).
    """
    try:
        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Tìm tất cả các thẻ <a> có thuộc tính href
        anchors = soup.find_all('a', href=True)
        if not anchors:
            return 0  # Không có anchor link, coi là legitimate
        
        total_anchors = len(anchors)
        null_anchors = sum(1 for a in anchors if a['href'].lower() in ['', '#', '#content', 'javascript:void(0)'])
        
        # Tính tỷ lệ null anchor link
        ratio = null_anchors / total_anchors if total_anchors > 0 else 0
        return ratio 
        
    except Exception as e:
        print(f"Lỗi khi xử lý HTML: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi
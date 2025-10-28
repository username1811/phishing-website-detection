def has_at_symbol(url):
    """
    Kiểm tra xem ký tự '@' có xuất hiện trong URL hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://legit.com@phish.com', 'http://www.example.com').
    
    Returns:
        bool: True nếu có ký tự '@' trong URL, False nếu không.
    """
    try:
        # Kiểm tra sự hiện diện của ký tự '@' trong toàn bộ URL
        return '@' in url
    
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://legit.com@phish.com",      # Có '@'
        "http://www.example.com",          # Không có '@'
        "https://user@domain.com",         # Có '@' (trong username)
        "http://sub.example.com/path",     # Không có '@'
        "invalid_url",                     # Lỗi (giả định)
    ]
    
    for url in urls:
        has_at = has_at_symbol(url)
        status = "Có '@'" if has_at else "Không '@'"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
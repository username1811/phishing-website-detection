import re

def has_double_slash_in_path(url):
    """
    Kiểm tra xem có hai dấu gạch chéo '//' xuất hiện trong phần path của URL hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://example.com//malicious', 'http://www.example.com/path').
    
    Returns:
        bool: True nếu có '//' trong path sau domain, False nếu không.
    """
    try:
        # Loại bỏ protocol (http://, https://) và lấy phần còn lại
        cleaned_url = re.sub(r'^https?://', '', url)
        
        # Tách hostname và path
        parts = cleaned_url.split('/')
        if len(parts) <= 1:  # Chỉ có domain, không có path
            return False
        
        # Lấy hostname (phần đầu tiên)
        hostname = parts[0]
        
        # Kết hợp lại path (bỏ hostname) và kiểm tra '//'
        path = '/' + '/'.join(parts[1:])  # Ghép lại path với dấu '/' đầu tiên
        
        # Kiểm tra sự hiện diện của '//' trong path (không tính '//' sau protocol)
        return '//' in path and not path.startswith('//')
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://example.com//malicious",      # Có '//' trong path
        "http://www.example.com/path",        # Không có '//'
        "http://example.com/sub//path",       # Có '//' trong path
        "http://example.com?param=//value",   # Không tính '//' trong query
        "http:////malicious.com",             # Không hợp lệ (// sau protocol)
        "invalid_url",                        # Lỗi (giả định)
    ]
    
    for url in urls:
        has_double_slash = has_double_slash_in_path(url)
        status = "Có '//' trong path" if has_double_slash else "Không có '//' trong path"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
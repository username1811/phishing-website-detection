import re

def is_tiny_url(url):
    """
    Kiểm tra xem URL có sử dụng dịch vụ rút gọn URL (bao gồm tinyURL) hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://tinyurl.com/abc123', 'https://www.example.com').
    
    Returns:
        bool: True nếu URL là dạng rút gọn (UF10 = 1), False nếu không (UF10 = 0).
    """
    try:
        # Loại bỏ protocol (http://, https://) và lấy hostname
        hostname = re.sub(r'^https?://', '', url).split('/')[0].lower()
        
        # Danh sách các dịch vụ rút gọn URL phổ biến (bao gồm tinyURL)
        shortening_services = [
            'tinyurl.com',
            'bit.ly',
            'goo.gl',
            't.co',
            'ow.ly',
            'is.gd',
            'w.wiki'  # Dịch vụ rút gọn của Wikipedia
        ]
        
        # Kiểm tra xem hostname có thuộc danh sách dịch vụ rút gọn không
        return hostname in shortening_services
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi (coi là không phải tiny URL)

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL (tính đến 02:45 PM +07, Chủ nhật, 26/10/2025)
    urls = [
        "http://tinyurl.com/abc123",      # tinyURL
        "https://www.example.com",        # Không phải rút gọn
        "http://bit.ly/xyz789",           # bit.ly
        "https://w.wiki/U",               # w.wiki
        "http://invalid.url",             # Lỗi (giả định)
    ]
    
    for url in urls:
        is_shortened = is_tiny_url(url)
        status = "shorten" if is_shortened else "normal"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
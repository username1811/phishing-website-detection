import re

def has_http_in_domain(url):
    """
    Kiểm tra xem 'http' hoặc 'https' có xuất hiện trong phần domain của URL hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://https-example.com', 'https://www.example.com').
    
    Returns:
        bool: True nếu 'http' hoặc 'https' xuất hiện trong domain, False nếu không.
    """
    try:
        # Loại bỏ protocol (http://, https://) và lấy hostname
        hostname = re.sub(r'^https?://', '', url).split('/')[0]
        
        # Kiểm tra sự hiện diện của 'http' hoặc 'https' trong hostname
        return bool(re.search(r'(http|https)', hostname, re.IGNORECASE))
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://https-example.com",         # Có 'https' trong domain
        "https://www.example.com",          # Không có trong domain (chỉ ở protocol)
        "http://http-sub.example.com",      # Có 'http' trong domain
        "https://secure.example.com",       # Không có trong domain
        "http://invalid.url",               # Lỗi (giả định)
    ]
    
    for url in urls:
        has_http = has_http_in_domain(url)
        status = "Có 'http/https' trong domain" if has_http else "Không có 'http/https' trong domain"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
import re

def has_dash_in_domain(url):
    """
    Kiểm tra xem có ký tự '-' xuất hiện trong phần domain của URL hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://login-bank.com', 'https://www.example.com').
    
    Returns:
        bool: True nếu có '-' trong domain (UF11 = 1), False nếu không (UF11 = 0).
    """
    try:
        # Loại bỏ protocol (http://, https://) và lấy hostname
        hostname = re.sub(r'^https?://', '', url).split('/')[0].lower()
        
        # Kiểm tra sự hiện diện của ký tự '-' trong hostname
        return '-' in hostname
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi (coi là không có '-')

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL (tính đến 02:34 PM +07, Chủ nhật, 26/10/2025)
    urls = [
        "http://login-bank.com",         # Có '-' trong domain
        "https://www.example.com",       # Không có '-'
        "http://pay-pal.com",            # Có '-' trong domain
        "https://sub.domain.com",        # Không có '-'
        "http://invalid.url",            # Lỗi (giả định)
        "http://paypal.com/menu/folder-1/",       
    ]
    
    for url in urls:
        has_dash = has_dash_in_domain(url)
        status = "Có '-' trong domain (UF11 = 1)" if has_dash else "Không có '-' trong domain (UF11 = 0)"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
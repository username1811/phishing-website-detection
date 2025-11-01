import re

def calculate_uf2(url):
    """
    Tính giá trị UF2 dựa trên số lượng dấu chấm trong hostname của URL.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://www.example.com' hoặc 'http://sub1.sub2.example.com.phish').
    
    Returns:
        float: Giá trị UF2 (0, 0.5, hoặc 1) theo quy tắc:
               - 0: Legitimate (dots <= 2)
               - 0.5: Suspicious (dots = 3)
               - 1: Phishing (dots > 3)
    """
    try:
        # Loại bỏ protocol (http://, https://) và lấy hostname
        hostname = re.sub(r'^https?://', '', url).split('/')[0]
        
        # Đếm số lượng dấu chấm trong hostname
        dot_count = hostname.count('.')
        return dot_count
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return 0  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://www.example.com",              # Legitimate
        "http://www.sub.example.com",          # Legitimate
        "http://www.sub.domain.example.com",   # Suspicious
        "http://sub1.sub2.example.com.phish",  # Phishing
        "http://invalid.url",                  # Lỗi (giả định)
    ]
    
    for url in urls:
        uf2_value = calculate_uf2(url)
        print(f"{url}: {uf2_value}\n")
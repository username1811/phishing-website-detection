import re

def calculate_uf5(url):
    """
    Tính giá trị UF5 dựa trên độ dài của URL.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://www.example.com', 'http://very.long.phishing.url.example.com').
    
    Returns:
        int: Giá trị UF5 (0, 0.5, hoặc 1) theo quy tắc:
             - 0: Legitimate (length < 75)
             - 0.5: Suspicious (75 <= length < 100)
             - 1: Phishing (length >= 100)
    """
    try:
        # Tính độ dài của toàn bộ URL (bao gồm protocol và các phần khác)
        hostname = re.sub(r'^https?://', '', url).split('/')[0]
        return len(hostname)
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return 0  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://www.example.com",              # Legitimate (dài 22)
        "http://sub.example.com/path",         # Legitimate (dài 28)
        "http://www.longer.example.com/path",  # Suspicious (dài 78)
        "http://very.long.phishing.url.example.com/path",  # Phishing (dài 120)
        "http://very.long.phishing.url.example.com/path/id?param=12334532452345",  # Phishing (dài 120)
        "invalid_url",                         # Lỗi (giả định)
    ]
    
    for url in urls:    
        uf5_value = calculate_uf5(url)
        print(f"url: {url} \nlength: {uf5_value}\n")
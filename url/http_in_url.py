import re

def is_phishing_by_scheme(url):
    """
    Kiểm tra giao thức của URL để xác định giá trị UF9.
    Trả về True nếu giao thức không phải 'https' (phishing, UF9 = 1),
    False nếu là 'https' (legitimate, UF9 = 0).
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'https://www.example.com', 'http://example.com').
    
    Returns:
        bool: True nếu giao thức là 'http' hoặc không xác định (phishing), False nếu là 'https' (legitimate).
    """
    try:
        # Kiểm tra giao thức bằng regex
        match = re.match(r'^(https?)://', url, re.IGNORECASE)
        if match:
            protocol = match.group(1).lower()
            return protocol != 'https'  # True nếu không phải 'https', False nếu là 'https'
        else:
            return True  # Không có protocol hoặc không hợp lệ, coi là phishing
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return True  # Giá trị mặc định nếu có lỗi (coi là phishing)

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL (tính đến 02:30 PM +07, Chủ nhật, 26/10/2025)
    urls = [
        "https://www.example.com",      # Legitimate (UF9 = 0)
        "http://example.com",           # Phishing (UF9 = 1)
        "ftp://example.com",            # Phishing (UF9 = 1)
        "www.example.com",             # Phishing (UF9 = 1, không có protocol)
        "invalid_url",                 # Lỗi (giả định)
    ]
    
    for url in urls:
        is_phishing = is_phishing_by_scheme(url)
        status = "Phishing (UF9 = 1)" if is_phishing else "Legitimate (UF9 = 0)"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
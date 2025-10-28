def has_uppercase_letter(url):
    """
    Kiểm tra xem URL có chứa chữ cái viết hoa hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://ExAmPlE.com', 'https://www.example.com').
    
    Returns:
        bool: True nếu có chữ cái viết hoa trong URL (UF13 = 1), False nếu không (UF13 = 0).
    """
    try:
        # Kiểm tra sự hiện diện của bất kỳ chữ cái viết hoa nào trong URL
        return any(char.isupper() for char in url if char.isalpha())
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi (coi là không có chữ viết hoa)

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL (tính đến 02:40 PM +07, Chủ nhật, 26/10/2025)
    urls = [
        "http://ExAmPlE.com",         # Có chữ viết hoa
        "https://www.example.com",    # Không có chữ viết hoa
        "http://LOGIN.example.com",   # Có chữ viết hoa
        "https://sub.domain.COM",     # Có chữ viết hoa
        "http://invalid.url",         # Lỗi (giả định)
    ]
    
    for url in urls:
        has_upper = has_uppercase_letter(url)
        status = "Có chữ viết hoa (UF13 = 1)" if has_upper else "Không có chữ viết hoa (UF13 = 0)"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
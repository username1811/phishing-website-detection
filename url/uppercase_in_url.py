from urllib.parse import urlparse

def has_uppercase_letter(url):
    """
    Kiểm tra xem DOMAIN của URL có chứa chữ cái viết hoa hay không.
    (Chỉ xét phần domain, KHÔNG xét path, query, fragment)

    Args:
        url (str): URL cần phân tích (ví dụ: 'http://ExAmPlE.com/path/ABC?Q=XYZ')

    Returns:
        bool: True nếu domain có chữ in hoa (UF13 = 1), False nếu không (UF13 = 0).
    """
    try:
        # Phân tích URL
        parsed = urlparse(url)
        domain = parsed.netloc  # Chỉ lấy phần domain (ví dụ: ExAmPlE.com)

        if not domain:
            return False

        # Kiểm tra có chữ cái in hoa trong domain
        return any(char.isupper() for char in domain if char.isalpha())

    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Mặc định: không có chữ in hoa


# === VÍ DỤ SỬ DỤNG ===
if __name__ == "__main__":
    urls = [
        "http://ExAmPlE.com",                    # True → domain có hoa
        "https://www.example.com",               # False → domain không hoa
        "https://www.example.com/YIUY",          # False → path có hoa, nhưng domain không
        "http://LOGIN.example.com",              # True → domain có hoa
        "https://sub.domain.COM/path",           # True → domain có hoa
        "http://example.com/ABC/DEF?Q=XYZ",      # False → chỉ path/query có hoa
        "http://invalid.url",                    # False → domain không hợp lệ
        "http://USER@password.com",              # True → USER có hoa
    ]

    print("KIỂM TRA CHỮ IN HOA TRONG DOMAIN (chỉ netloc)\n")
    for url in urls:
        has_upper = has_uppercase_letter(url)
        status = "Có chữ in hoa (UF13 = 1)" if has_upper else "Không có chữ in hoa (UF13 = 0)"
        print(f"URL: {url}")
        print(f"   → Domain: {urlparse(url).netloc}")
        print(f"   → Kết quả: {status}\n")
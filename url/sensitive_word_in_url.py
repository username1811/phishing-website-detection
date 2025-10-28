import re

def has_sensitive_word(url):
    """
    Kiểm tra xem URL có chứa từ nhạy cảm (phishing terms) hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://login.example.com', 'https://www.example.com').
    
    Returns:
        bool: True nếu có từ nhạy cảm trong URL (UF12 = 1), False nếu không (UF12 = 0).
    """
    try:
        # Chuyển URL thành chữ thường để kiểm tra không phân biệt hoa/thường
        url_lower = url.lower()
        
        # Danh sách từ nhạy cảm (phishing terms) - mở rộng dựa trên ví dụ
        sensitive_words = [
            'login', 'update', 'validate', 'activate', 'secure',
            'account', 'verify', 'password', 'signin', 'confirm',
            'payment', 'bank', 'credit', 'debit', 'transaction',
            'alert', 'error', 'support'  # Điền đủ 18 từ dựa trên giả định
        ]
        
        # Kiểm tra sự hiện diện của bất kỳ từ nhạy cảm nào trong URL
        return any(word in url_lower for word in sensitive_words)
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi (coi là không có từ nhạy cảm)

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL (tính đến 02:37 PM +07, Chủ nhật, 26/10/2025)
    urls = [
        "http://login.example.com",         # Có 'login'
        "https://www.example.com",          # Không có từ nhạy cảm
        "http://update-account.com",        # Có 'update' và 'account'
        "https://secure.payment.bank",      # Có 'secure', 'payment', 'bank'
        "http://invalid.url",               # Lỗi (giả định)
    ]
    
    for url in urls:
        has_sensitive = has_sensitive_word(url)
        status = "Có từ nhạy cảm (UF12 = 1)" if has_sensitive else "Không có từ nhạy cảm (UF12 = 0)"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
import re
import ipaddress

def has_ip_in_domain(url):
    """
    Kiểm tra xem địa chỉ IP (IPv4 hoặc IPv6) có xuất hiện trong phần domain của URL hay không.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://192.168.1.1', 'http://www.example.com', 'http://[2001:db8::1]').
    
    Returns:
        bool: True nếu có IP trong domain, False nếu không.
    """
    try:
        # Loại bỏ protocol (http://, https://) và lấy hostname
        hostname = re.sub(r'^https?://', '', url).split('/')[0]
        
        # Kiểm tra IPv4
        ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        if re.match(ipv4_pattern, hostname):
            try:
                ipaddress.IPv4Address(hostname)  # Kiểm tra xem có hợp lệ không
                return True
            except ValueError:
                pass  # Không phải IPv4 hợp lệ
        
        # Kiểm tra IPv6 (bao gồm cả dạng với dấu ngoặc vuông [ ])
        ipv6_pattern = r'^\[?[0-9a-fA-F:]+]?$'
        if re.match(ipv6_pattern, hostname):
            try:
                ipaddress.IPv6Address(hostname.strip('[]'))  # Loại bỏ [] và kiểm tra
                return True
            except ValueError:
                pass  # Không phải IPv6 hợp lệ
        
        return False  # Không có IP
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://192.168.1.1",              # Có IPv4
        "http://www.example.com",          # Không có IP
        "http://[2001:db8::1]",            # Có IPv6
        "http://sub.example.com",          # Không có IP
        "http://256.256.256.256",          # Không hợp lệ (giả định)
    ]
    
    for url in urls:
        has_ip = has_ip_in_domain(url)
        status = "Có IP" if has_ip else "Không có IP"
        print(f"URL: {url}")
        print(f"Kết quả: {status}\n")
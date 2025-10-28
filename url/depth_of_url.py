import re

def calculate_uf6(url):
    """
    Tính độ sâu (số lượng subpages/subfolders) trong phần path của URL.
    
    Args:
        url (str): URL cần phân tích (ví dụ: 'http://example.com/sub1/sub2/page.html').
    
    Returns:
        int: Số lượng subpages/subfolders trong path (0 nếu không có path hoặc lỗi).
    """
    try:
        # Loại bỏ protocol (http://, https://) và query string (nếu có)
        cleaned_url = re.sub(r'^https?://', '', url).split('?')[0]
        
        # Tách hostname và path
        parts = cleaned_url.split('/')
        if len(parts) <= 1:  # Chỉ có domain, không có path
            return 0
        
        # Lấy phần path (bỏ qua hostname và phần rỗng)
        path_parts = [part for part in parts[1:] if part]  # Bỏ phần rỗng sau split
        
        # Độ sâu là số lượng subpages/subfolders (không tính file cuối nếu là file)
        if path_parts and '.' in path_parts[-1]:  # Nếu phần cuối là file (có dấu chấm)
            return len(path_parts) - 1  # Không tính file cuối
        else:
            return len(path_parts)  # Tính tất cả nếu không có file
        
    except Exception as e:
        print(f"Lỗi khi xử lý URL: {str(e)}")
        return 0  # Giá trị mặc định nếu có lỗi

# Ví dụ sử dụng
if __name__ == "__main__":
    # Các ví dụ URL
    urls = [
        "http://example.com",                       # Không có path
        "http://example.com/sub1/sub2",             # 2 subfolders
        "http://example.com/sub1/sub2/page.html",   # 2 subfolders (không tính file)
        "http://example.com/sub1/sub2/?id=1",       # 2 subfolders
        "http://example.com/sub1//sub2",            # 2 subfolders (xử lý double slash)
        "invalid_url",                             # Lỗi (giả định)
    ]
    
    for url in urls:
        uf6_value = calculate_uf6(url)
        print(f"URL: {url}")
        print(f"UF6 (Độ sâu): {uf6_value}\n")
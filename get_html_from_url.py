# get_html_from_url.py
import pandas as pd
import os

# === CẤU HÌNH ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Thư mục gốc project
CSV_FILE = os.path.join(BASE_DIR, 'phishing_metadata.csv')  # File CSV gốc

# Đọc CSV một lần để cache (tăng tốc)
df = pd.read_csv(CSV_FILE)

# Chuẩn hóa cột url (loại bỏ khoảng trắng)
df['url'] = df['url'].astype(str).str.strip()
df['html_path'] = df['html_path'].astype(str).replace('nan', '')

# Tạo dictionary ánh xạ: url -> html_path
URL_TO_HTML = dict(zip(df['url'], df['html_path']))

def get_html_content(url):
    """
    Nhận vào một URL (string), trả về nội dung file HTML (string) nếu tồn tại.
    
    Args:
        url (str): URL từ file CSV
    
    Returns:
        str: Nội dung HTML (hoặc "" nếu không có file)
    """
    url = str(url).strip()
    
    # Lấy html_path từ ánh xạ
    html_path = URL_TO_HTML.get(url, "")
    
    # Nếu không có html_path → trả về rỗng
    if not html_path or html_path == 'nan' or html_path == '':
        return ""
    
    # Chuẩn hóa đường dẫn (Windows: \, Linux: /)
    html_path = html_path.replace('\\', os.sep).replace('/', os.sep)
    full_path = os.path.join(BASE_DIR, html_path)
    
    # Kiểm tra file tồn tại
    if not os.path.isfile(full_path):
        print(f"[!] Không tìm thấy file: {full_path}")
        return ""
    
    # Đọc file HTML
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"[!] Lỗi đọc file {full_path}: {e}")
        return ""
    
#print(get_html_content('http://www.academickids.com/encyclopedia/index.php/Connectedness'));
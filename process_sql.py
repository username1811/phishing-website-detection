import mysql.connector
import pandas as pd
import os

# Kết nối MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Thay bằng username MySQL (thường là 'root')
    password="matkhaumoi1811",  # Thay bằng password MySQL
    database="phishing_dataset"
)

# Query toàn bộ bảng index
df = pd.read_sql_query("SELECT * FROM `index`", conn)

# Đóng kết nối
conn.close()

# Thêm cột đường dẫn HTML
def get_html_path(website):
    folder = 'folder1'  # Chỉ kiểm tra folder1 vì bạn đã sửa
    path = os.path.join(folder, website)
    if os.path.exists(path):
        return path
    return None

df['html_path'] = df['website'].apply(get_html_path)

# Lưu thành CSV
df.to_csv('phishing_metadata.csv', index=False, encoding='utf-8')
print("Đã tạo file phishing_metadata.csv")
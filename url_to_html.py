import requests
from bs4 import BeautifulSoup

def get_html_from_url(url):
    try:
        # Gửi yêu cầu HTTP đến URL
        response = requests.get(url)
        # Kiểm tra mã trạng thái
        if response.status_code == 200:
            # Lấy nội dung HTML
            html_content = response.text
            # Tạo đối tượng BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            # In nội dung HTML với định dạng đẹp
            print(soup.prettify())
            return soup
        else:
            return f"Lỗi: Mã trạng thái {response.status_code}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

# Sử dụng
url = input("Nhập URL của website: ")  # Nhập URL từ người dùng
result = get_html_from_url(url)

# Kiểm tra lỗi
if isinstance(result, str):
    print(result)
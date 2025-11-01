from bs4 import BeautifulSoup

def is_suspicious_form_action(html_content):
    """
    Kiểm tra xem trường 'action' của thẻ <form> có chứa dấu hiệu phishing hay không.
    
    Args:
        html_content (str): Nội dung HTML của trang web.
    
    Returns:
        bool: True nếu có external link, PHP file, '', '#', hoặc 'javascript:void(0)' (HF5 = 1),
              False nếu không (HF5 = 0).
    """
    try:
        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Tìm tất cả các thẻ <form>
        forms = soup.find_all('form')
        if not forms:
            return False  # Không có form, coi là legitimate
        
        # Kiểm tra trường 'action' của từng form
        for form in forms:
            action = form.get('action', '').lower()
            if (action and (  # Kiểm tra external link hoặc PHP
                'http' in action or '.php' in action
            )) or action in ['', '#', 'javascript:void(0)']:
                return True  # Tìm thấy dấu hiệu phishing
        return False  # Không có dấu hiệu phishing
        
    except Exception as e:
        print(f"Lỗi khi xử lý HTML: {str(e)}")
        return False  # Giá trị mặc định nếu có lỗi



# Ví dụ sử dụng
if __name__ == "__main__":
    # Ví dụ HTML mẫu
    html_samples = [
        """
        <html><body>
            <form action="http://external.com/login.php"></form>
        </body></html>
        """,  # HF5 = 1 (external link và PHP)
        """
        <html><body>
            <form action="/login"></form>
        </body></html>
        """,  # HF5 = 0 (internal link)
        """
        <html><body>
            <a href="#"></a><a href="#content"></a><a href="page.html"></a>
        </body></html>
        """,  # HF6 = 1 (2/3 > 0.34)
        """
        <html><body>
            <a href="page.html"></a><a href="another.html"></a>
        </body></html>
        """,  # HF6 = 0 (0/2 = 0)
    ]
    
    for i, html in enumerate(html_samples, 1):
        print(f"HTML Sample {i}:")
        print(f"HTML Sample {html}:")
        hf5_value = is_suspicious_form_action(html)
        print(f"form is suspicious" if hf5_value else 'form is normal')
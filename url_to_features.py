import os
import urllib.parse
import requests
import joblib
import numpy as np
import pandas as pd
import warnings  # Thêm để tắt cảnh báo

# Tắt cảnh báo cụ thể (tạm thời, chỉ cho validation)
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.utils.validation")

# Import các hàm từ module tùy chỉnh (giả định đã có file url.py và hyperlink.py)
from hyperlink import external_hyperlink_ratio, null_link, suspicious_form_action
from url import (
    atsign_in_url, count_dot_in_url, dash_in_url, depth_of_url,
    http_in_url, ip_in_url, length_of_url, redirection_in_url,
    sensitive_word_in_url, shorten_url, uppercase_in_url
)

# Danh sách thứ tự features (phải khớp với X.columns trong train - kiểm tra và cập nhật nếu cần)
FEATURE_ORDER = [
    'atsign_in_url', 'count_dot_in_url', 'dash_in_url', 'depth_of_url',
    'http_in_url', 'ip_in_url', 'length_of_url', 'redirection_in_url',
    'sensitive_word_in_url', 'shorten_url', 'uppercase_in_url',
    'external_hyperlink_ratio', 'suspicious_form_action', 'null_link_ratio'
]

# === HÀM TRÍCH XUẤT ĐẶC TRƯNG (giữ nguyên) ===
def extract_features(url, html_content=None):
    features = {}

    # === TRÍCH XUẤT ĐẶC TRƯNG TỪ URL ===
    features['atsign_in_url'] = 1 if atsign_in_url.has_at_symbol(url) else 0
    features['count_dot_in_url'] = count_dot_in_url.calculate_uf2(url)
    features['dash_in_url'] = 1 if dash_in_url.has_dash_in_domain(url) else 0
    features['depth_of_url'] = depth_of_url.calculate_uf6(url)
    features['http_in_url'] = 1 if http_in_url.is_phishing_by_scheme(url) else 0
    features['ip_in_url'] = 1 if ip_in_url.has_ip_in_domain(url) else 0
    features['length_of_url'] = length_of_url.calculate_uf5(url)
    features['redirection_in_url'] = 1 if redirection_in_url.has_double_slash_in_path(url) else 0
    features['sensitive_word_in_url'] = 1 if sensitive_word_in_url.has_sensitive_word(url) else 0
    features['shorten_url'] = 1 if shorten_url.is_tiny_url(url) else 0
    features['uppercase_in_url'] = 1 if uppercase_in_url.has_uppercase_letter(url) else 0

    # === TRÍCH XUẤT ĐẶC TRƯNG TỪ HTML ===
    if html_content:
        try:
            parsed_url = urllib.parse.urlparse(url)
            domain = parsed_url.netloc.lower()

            ratio = external_hyperlink_ratio.GetExternalHyperlinkRatio(html_content, domain)
            form_action = suspicious_form_action.is_suspicious_form_action(html_content)
            null_link_ratio = null_link.null_link_ratio(html_content)

            features['external_hyperlink_ratio'] = ratio
            features['suspicious_form_action'] = 1 if form_action else 0
            features['null_link_ratio'] = null_link_ratio
        except Exception as e:
            print(f"[Lỗi trích xuất HTML cho {url}]: {e}")
            features['external_hyperlink_ratio'] = 0.0
            features['suspicious_form_action'] = 0
            features['null_link_ratio'] = 0.0
    else:
        print(f"[Không có HTML] cho URL: {url}")
        features['external_hyperlink_ratio'] = 0.0
        features['suspicious_form_action'] = 0
        features['null_link_ratio'] = 0.0

    return features

# === HÀM CHUYỂN DICT THÀNH DATAFRAME HOẶC ARRAY (sửa để debug và fallback) ===
def features_to_input(features_dict, model):
    feature_values = [features_dict.get(feat, 0) for feat in FEATURE_ORDER]
    
    # Thử dùng DataFrame với tên cột
    try:
        feature_df = pd.DataFrame([feature_values], columns=FEATURE_ORDER)
        
        # Debug: Kiểm tra nếu model có feature_names_in_ (sklearn >=1.0)
        if hasattr(model, 'feature_names_in_'):
            expected_names = model.feature_names_in_
            if list(feature_df.columns) != list(expected_names):
                print(f"⚠️ Cảnh báo: Tên cột predict ({feature_df.columns.tolist()}) không khớp train ({expected_names.tolist()}). Sử dụng array fallback.")
                return np.array(feature_values).reshape(1, -1)
        
        print("✅ Tên cột khớp, sử dụng DataFrame.")
        return feature_df
    except Exception as e:
        print(f"❌ Lỗi tạo DataFrame: {e}. Sử dụng array fallback.")
        return np.array(feature_values).reshape(1, -1)

# === HÀM FETCH HTML TỪ URL (giữ nguyên) ===
def get_html_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Lỗi: Mã trạng thái HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Lỗi kết nối: {str(e)}")
        return None

# === HÀM DỰ ĐOÁN (sửa để nhận input linh hoạt) ===
def predict_phishing(model, features_input):
    prediction = model.predict(features_input)[0]
    probabilities = model.predict_proba(features_input)[0]
    
    label = "Phishing (1)" if prediction == 1 else "Benign (0)"
    prob_phishing = probabilities[1]
    prob_benign = probabilities[0]
    
    return prediction, label, prob_phishing, prob_benign

# === CHƯƠNG TRÌNH CHÍNH ===
if __name__ == "__main__":
    # Load mô hình
    try:
        model = joblib.load("rf_phishing_model.pkl")
        print("✅ Đã load mô hình Random Forest.")
        
        # Debug: In expected feature names nếu có
        if hasattr(model, 'feature_names_in_'):
            print(f"📋 Tên đặc trưng từ model: {model.feature_names_in_.tolist()}")
        else:
            print("📋 Model không lưu tên đặc trưng (sklearn cũ). Đảm bảo FEATURE_ORDER đúng.")
            
    except FileNotFoundError:
        print("❌ Không tìm thấy file model 'rf_phishing_model.pkl'. Hãy chạy script train trước!")
        exit()
    except Exception as e:
        print(f"❌ Lỗi load model: {e}")
        exit()
    
    url = input("Nhập URL của website: ").strip()
    if not url:
        print("URL không được để trống!")
        exit()
    
    # Thêm scheme nếu thiếu
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"Đang fetch HTML từ: {url}")
    html_content = get_html_content(url)
    
    features_dict = extract_features(url, html_content)
    features_input = features_to_input(features_dict, model)
    
    print("\n=== CÁC ĐẶC TRƯNG TRÍCH XUẤT ===")
    for key, value in features_dict.items():
        print(f"{key}: {value}")
    
    # Dự đoán
    prediction, label, prob_phishing, prob_benign = predict_phishing(model, features_input)
    
    print("\n=== KẾT QUẢ DỰ ĐOÁN ===")
    print(f"Nhãn dự đoán: {label}")
    print(f"Xác suất Benign: {prob_benign:.2%}")
    print(f"Xác suất Phishing: {prob_phishing:.2%}")
    
    if prediction == 1:
        print("⚠️  CẢNH BÁO: URL này có nguy cơ cao là phishing! Không nhập thông tin cá nhân.")
    else:
        print("✅ URL có vẻ an toàn.")
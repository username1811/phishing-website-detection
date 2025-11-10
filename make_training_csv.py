# make_training_csv.py
import pandas as pd
import os
import urllib.parse
from hyperlink import external_hyperlink_ratio, null_link,  suspicious_form_action
from url import (
    atsign_in_url, count_dot_in_url, dash_in_url, depth_of_url,
    http_in_url, ip_in_url, length_of_url, redirection_in_url,
    sensitive_word_in_url, shorten_url, uppercase_in_url
)

# === HÀM TRÍCH XUẤT ĐẶC TRƯNG ===
def extract_features(url, html_path=None, base_dir=""):
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
    html_content = None
    if html_path and pd.notna(html_path):
        full_path = os.path.join(base_dir, str(html_path).strip().replace('\\', os.sep))
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    html_content = f.read()
            except Exception as e:
                print(f"[Lỗi đọc file HTML {full_path}]: {e}")
        else:
            print(f"[Không tìm thấy file HTML]: {full_path}")
    else:
        print(f"[HTML trống] cho URL: {url}")

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
            features['null_link_ratio'] = 0
    else:
        features['external_hyperlink_ratio'] = 0.0
        features['suspicious_form_action'] = 0
        features['null_link_ratio'] = 0

    return features

# === HÀM CHÍNH: TẠO FILE CSV HUẤN LUYỆN (TEST 100 MẪU) ===
def create_training_csv_test(input_csv, output_csv, base_dir="", limit=100):
    # Đọc file CSV
    print(f"Đang đọc file: {input_csv}")
    df = pd.read_csv(input_csv)

    # Chỉ lấy 100 dòng đầu
    df = df.head(limit)
    print(f"ĐÃ LẤY {len(df)} MẪU ĐẦU TIÊN ĐỂ TEST\n")

    feature_list = []

    for idx, row in df.iterrows():
        url = row['url']
        html_path = row.get('html_path')
        label = row['result']

        print(f"[{idx+1}/{len(df)}] Đang xử lý: {url}")

        features = extract_features(url, html_path, base_dir)
        features['label'] = label
        feature_list.append(features)

        # In mẫu đầu tiên để kiểm tra
        if idx == 0:
            print("\nMẪU ĐẶC TRƯNG ĐẦU TIÊN:")
            for k, v in features.items():
                print(f"  • {k}: {v}")
            print()

    # Tạo DataFrame
    feature_df = pd.DataFrame(feature_list)
    cols = [col for col in feature_df.columns if col != 'label'] + ['label']
    feature_df = feature_df[cols]

    # Lưu file
    feature_df.to_csv(output_csv, index=False)
    print(f"\nHOÀN TẤT TEST! Đã lưu {len(feature_df)} mẫu vào: {output_csv}")
    print(f"File có {len(feature_df.columns)} cột: {list(feature_df.columns)}")
    print(f"\nMỞ file '{output_csv}' để kiểm tra kết quả!")

# === CHẠY TEST ===
if __name__ == "__main__":
    INPUT_CSV = "phishing_metadata.csv"      # Đảm bảo file này tồn tại
    OUTPUT_CSV = "training_features_test.csv"  # File test
    BASE_DIR = "."                            # Thư mục chứa dataset-part-*

    create_training_csv_test(INPUT_CSV, OUTPUT_CSV, BASE_DIR, limit=80000)
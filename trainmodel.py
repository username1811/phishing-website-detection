# ==============================
#  Train Random Forest on Phishing Dataset (Chỉ Recall)
# ==============================

# Import thư viện
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, recall_score
import joblib

# ======================================
# 1️⃣ Đọc dữ liệu
# ======================================
data = pd.read_csv("training_features_test.csv")

# Hiển thị 5 dòng đầu
print(data.head())

# ======================================
# 2️⃣ Chuẩn bị dữ liệu
# ======================================
X = data.drop(columns=['label'])
y = data['label']

# Chia tập train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, shuffle=True, stratify=y
)

# ======================================
# 3️⃣ Huấn luyện mô hình Random Forest (ưu tiên recall)
# ======================================
rf_model = RandomForestClassifier(
    n_estimators=300, 
    max_depth=29, 
    random_state=42,
    bootstrap=True,
    class_weight='balanced'  # Tăng recall cho class thiểu số (phishing)
)

rf_model.fit(X_train, y_train)

# ======================================
# 4️⃣ Đánh giá mô hình (chỉ Recall + Confusion Matrix)
# ======================================
y_pred = rf_model.predict(X_test)

# Recall cho class 1 (phishing)
recall_phishing = recall_score(y_test, y_pred)

# Recall trên tập train (kiểm tra overfitting)
train_recall = recall_score(y_train, rf_model.predict(X_train))
print("Recall Phishing trên tập huấn luyện:", train_recall)

print("Recall Phishing trên tập kiểm tra:", recall_phishing)
print("\n📋 Báo cáo phân loại:\n", classification_report(y_test, y_pred))

# Confusion Matrix (xem FN)
cm = confusion_matrix(y_test, y_pred)
print("\n🔍 Confusion Matrix:\n", cm)
# [[TN, FP], [FN, TP]] - Tập trung FN thấp

# # ======================================
# # 5️⃣ Tinh chỉnh tham số (GridSearchCV - chỉ Recall)
# # ======================================
# param_grid = {
#     'max_depth': [9,13,17,21,25,29,33, None],
#     'n_estimators': [100, 200, 300, 400],
#     'max_features': ['sqrt', 'log2']
# }

# grid_search = GridSearchCV(
#     estimator=RandomForestClassifier(random_state=42, class_weight='balanced'),
#     param_grid=param_grid,
#     cv=5,
#     scoring='recall',  # Chỉ recall cho class 1
#     n_jobs=-1
# )

# grid_search.fit(X_train, y_train)

# print("✅ Tham số tốt nhất:", grid_search.best_params_)
# print("🎯 Recall tốt nhất (cho Phishing):", grid_search.best_score_)

# # Lưu model
# best_model = grid_search.best_estimator_
# joblib.dump(best_model, "rf_phishing_model.pkl")
# print("💾 Model saved as rf_phishing_model.pkl")

# # ======================================
# # 6️⃣ Kiểm tra tầm quan trọng của đặc trưng
# # ======================================
# feature_importance = pd.DataFrame({
#     'Feature': X.columns,
#     'Importance': best_model.feature_importances_
# }).sort_values(by='Importance', ascending=False)

# plt.figure(figsize=(10,5))
# sns.barplot(x='Importance', y='Feature', data=feature_importance)
# plt.title('Feature Importance in Random Forest')
# plt.show()
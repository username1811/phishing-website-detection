# ==============================
#  Train Random Forest on Phishing Dataset
# ==============================

# Import thư viện
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# ======================================
# 1️⃣ Đọc dữ liệu
# ======================================
# Giả sử bạn đã lưu file CSV (ví dụ: phishing_dataset.csv)
# -> Nếu bạn có file Excel, thay read_csv bằng read_excel
data = pd.read_csv("training_features_test.csv")

# Hiển thị 5 dòng đầu
print(data.head())

# ======================================
# 2️⃣ Chuẩn bị dữ liệu
# ======================================
# Giả sử cột nhãn là 'label'
X = data.drop(columns=['label'])
y = data['label']

# Chia tập train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, shuffle=True, stratify=y
)

# ======================================
# 3️⃣ Huấn luyện mô hình Random Forest
# ======================================
rf_model = RandomForestClassifier(
    n_estimators=100, 
    max_depth=7, 
    random_state=42,
    bootstrap=True
)

rf_model.fit(X_train, y_train)

# ======================================
# 4️⃣ Đánh giá mô hình
# ======================================
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("🎯 Độ chính xác trên tập kiểm tra:", accuracy)
print("\n📋 Báo cáo phân loại:\n", classification_report(y_test, y_pred))

# Kiểm tra overfitting
train_acc = rf_model.score(X_train, y_train)
print("Độ chính xác trên tập huấn luyện:", train_acc)

# ======================================
# 5️⃣ Tinh chỉnh tham số (GridSearchCV)
# ======================================
param_grid = {
    'max_depth': [3, 5, 7, 9, 11, None],
    'n_estimators': [50, 100, 200],
    'max_features': ['sqrt', 'log2']
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=5,
    scoring='recall',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("✅ Tham số tốt nhất:", grid_search.best_params_)
print("🎯 Độ chính xác tốt nhất:", grid_search.best_score_)

# Lưu model tốt nhất
best_model = grid_search.best_estimator_
joblib.dump(best_model, "rf_phishing_model.pkl")
print("💾 Model saved as rf_phishing_model.pkl")

# ======================================
# 6️⃣ Kiểm tra tầm quan trọng của đặc trưng
# ======================================
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': best_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10,5))
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title('Feature Importance in Random Forest')
plt.show()

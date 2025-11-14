import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc, recall_score, classification_report

def show_charts():
    """
    Hàm load mô hình RF đã train và hiển thị charts: Feature Importance, Confusion Matrix, ROC Curve.
    Không cần train lại, chỉ predict trên test set.
    """
    # Bước 1: Load mô hình từ file .pkl (sử dụng joblib như code train)
    model = joblib.load("rf_phishing_model.pkl")
    print("✅ Mô hình đã được load thành công!")

    # Bước 2: Load dữ liệu và chia train/test giống hệt lúc train (random_state=42, stratify=y)
    data = pd.read_csv("training_features_test.csv")
    X = data.drop(columns=['label'])
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, shuffle=True, stratify=y
    )
    feature_names = X.columns.tolist()  # Tên features cho chart

    # Bước 3: Predict trên test set (không train lại)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]  # Xác suất class 1 (phishing)

    # Tính recall phishing (giống code train)
    recall_phishing = recall_score(y_test, y_pred)
    print("Recall Phishing trên tập kiểm tra:", recall_phishing)
    print("\n📋 Báo cáo phân loại:\n", classification_report(y_test, y_pred))
    print("\n🔍 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Chart 1: Feature Importance (Bar chart, sắp xếp giảm dần)
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=importance_df)
    plt.title('Feature Importance trong mô hình Phishing Detection')
    plt.xlabel('Độ quan trọng')
    plt.tight_layout()
    plt.show()

    # Chart 2: Confusion Matrix (Heatmap, tập trung FN thấp cho recall cao)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Legit (0)', 'Phishing (1)'], 
                yticklabels=['Legit (0)', 'Phishing (1)'])
    plt.title('Confusion Matrix (Tập trung FN thấp)')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

    # Chart 3: ROC Curve (Đo lường khả năng phân biệt class)
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (Tỷ lệ FP)')
    plt.ylabel('True Positive Rate (Recall)')
    plt.title('ROC Curve cho mô hình Phishing (AUC cao = tốt)')
    plt.legend(loc="lower right")
    plt.show()

    print(f"🎯 AUC Score: {roc_auc:.4f} (Càng gần 1 càng tốt)")

# Gọi hàm để show charts
if __name__ == "__main__":
    show_charts()
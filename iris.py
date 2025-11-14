# ==========================
# ĐỒ ÁN: SO SÁNH RANDOM FOREST vs SVM TRÊN TẬP IRIS
# Biểu đồ so sánh: CẠNH NHAU (subplot) - Không chồng nữa!
# ==========================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.inspection import permutation_importance
import warnings
warnings.filterwarnings('ignore')

# -----------------------------
# 1. Tải dữ liệu Iris
# -----------------------------
iris = datasets.load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print(f"Iris Dataset: {X.shape[0]} mẫu, {X.shape[1]} đặc trưng")
print(f"3 lớp: {target_names}")

# -----------------------------
# 2. Chia dữ liệu + Chuẩn hóa
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# 3. Huấn luyện 2 mô hình
# -----------------------------
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel='rbf', probability=True, random_state=42)
}

results = {}

print("\n" + "="*60)
print("KẾT QUẢ HUẤN LUYỆN")
print("="*60)

for name, model in models.items():
    print(f"\n--- {name} ---")
    if name == "SVM":
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_score = model.predict_proba(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_score = model.predict_proba(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    results[name] = {'model': model, 'y_pred': y_pred, 'y_score': y_score, 'accuracy': acc}
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=target_names, digits=3))

# -----------------------------
# 4. Confusion Matrix - 2 biểu đồ cạnh nhau
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
cmap_rf = sns.color_palette("Blues", as_cmap=True)
cmap_svm = sns.color_palette("Oranges", as_cmap=True)

for idx, (name, color_map) in enumerate(zip(["Random Forest", "SVM"], [cmap_rf, cmap_svm])):
    cm = confusion_matrix(y_test, results[name]['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap=color_map, ax=axes[idx],
                xticklabels=target_names, yticklabels=target_names, cbar=False)
    axes[idx].set_title(f"{name}\nAccuracy: {results[name]['accuracy']:.4f}", fontsize=14)
    axes[idx].set_xlabel("Dự đoán")
    axes[idx].set_ylabel("Thực tế")

plt.suptitle("So sánh Confusion Matrix", fontsize=18, y=1.05)
plt.tight_layout()
plt.show()

# -----------------------------
# 5. ROC Curve - 2 biểu đồ riêng biệt cạnh nhau
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
colors = ['aqua', 'darkorange', 'cornflowerblue']

for idx, name in enumerate(["Random Forest", "SVM"]):
    ax = axes[idx]
    y_score = results[name]['y_score']
    for i in range(3):
        fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=colors[i], lw=2,
                label=f'{target_names[i]} (AUC = {roc_auc:.3f})')
    
    ax.plot([0, 1], [0, 1], 'k--', lw=2, alpha=0.7)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title(f'ROC Curve - {name}')
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

plt.suptitle("So sánh ROC Curve Multiclass (2 biểu đồ riêng)", fontsize=18, y=1.02)
plt.tight_layout()
plt.show()

# -----------------------------
# 6. Feature Importance - 2 biểu đồ cạnh nhau
# -----------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Random Forest
importances_rf = results["Random Forest"]['model'].feature_importances_
idx_rf = np.argsort(importances_rf)[::-1]
sns.barplot(x=importances_rf[idx_rf], y=np.array(feature_names)[idx_rf], ax=ax1, palette="viridis")
ax1.set_title("Feature Importance - Random Forest (Gini)", fontsize=14)
ax1.set_xlabel("Độ quan trọng")

# SVM - Permutation Importance
perm = permutation_importance(results["SVM"]['model'], X_test_scaled, y_test, n_repeats=30, random_state=42)
idx_svm = np.argsort(perm.importances_mean)[::-1]
sns.barplot(x=perm.importances_mean[idx_svm], y=np.array(feature_names)[idx_svm], ax=ax2, palette="magma")
ax2.set_title("Feature Importance - SVM (Permutation)", fontsize=14)
ax2.set_xlabel("Giảm accuracy khi xáo trộn")

plt.suptitle("So sánh Tầm quan trọng đặc trưng", fontsize=18, y=1.02)
plt.tight_layout()
plt.show()

# -----------------------------
# 7. Learning Curve - 2 biểu đồ riêng cạnh nhau (DÙNG PIPELINE - KHÔNG LỖI)
# -----------------------------
from sklearn.pipeline import make_pipeline

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for idx, (name, color) in enumerate(zip(["Random Forest", "SVM"], ['red', 'blue'])):
    if name == "SVM":
        estimator = make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, random_state=42))
    else:
        estimator = RandomForestClassifier(n_estimators=100, random_state=42)
    
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy'
    )
    
    axes[idx].plot(train_sizes, train_scores.mean(axis=1), 'o-', color=color, label='Train', alpha= 0.9)
    axes[idx].plot(train_sizes, val_scores.mean(axis=1), 's-', color=color, label='Validation', alpha=0.9)
    axes[idx].set_title(f"Learning Curve - {name}")
    axes[idx].set_xlabel("Số mẫu huấn luyện")
    axes[idx].set_ylabel("Accuracy")
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)
    axes[idx].set_ylim(0.2, 1.05)

plt.suptitle("So sánh Learning Curve (2 biểu đồ riêng)", fontsize=18, y=1.02)
plt.tight_layout()
plt.show()

# -----------------------------
# 8. Tổng kết
# -----------------------------
print("\n" + "="*70)
print("TỔNG KẾT ĐỒ ÁN")
print("="*70)
for name in models.keys():
    print(f"{name:15}: Accuracy = {results[name]['accuracy']:.4f}")
print("-"*70)
print("Kết luận: Cả hai mô hình đều đạt hiệu suất gần hoàn hảo trên tập Iris.")
print("Random Forest thường dễ giải thích hơn nhờ Feature Importance tự nhiên.")
print("SVM mạnh về biên quyết định, nhưng cần scale dữ liệu.")
print("=> Phù hợp cho đồ án phân loại đa lớp với dữ liệu nhỏ và sạch!")
print("="*70)
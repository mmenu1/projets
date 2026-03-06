import pandas as pd

df = pd.read_csv("credit_knn/GermanCredit.csv")

print(df.head())
print(df.info())

X = df.drop("credit_risk", axis=1)  # toutes les colonnes sauf la cible
y = df["credit_risk"]               # colonne cible

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

num_cols = ["duration","amount","age","installment_rate","present_residence","number_credits","people_liable"]
cat_cols = [c for c in X.columns if c not in num_cols]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(), cat_cols)
])  #normalisation des variables numériques et encodage des variables catégorielles, sans quoi amount domine complètement le calcul de distance sur age par exemple.

X_processed = preprocessor.fit_transform(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, stratify=y, random_state=42
)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

k = 18 
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

k_range = range(1, 51)
scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy').mean()
    scores.append(score)

plt.plot(k_range, scores)
plt.xlabel("k")
plt.ylabel("Accuracy (CV)")
plt.title("Choix du meilleur k")
plt.show()

best_k = k_range[scores.index(max(scores))]
print(f"Meilleur k : {best_k}")

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
#plt.show()


#évalutation de l'overfitting (train vs test) en fonction de k

train_scores = []
test_scores  = []

for k in range(1, 51):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    train_scores.append(accuracy_score(y_train, knn.predict(X_train)))
    test_scores.append(accuracy_score(y_test,  knn.predict(X_test)))

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(range(1, 51), train_scores, label="Train", marker='o', markersize=4)
ax.plot(range(1, 51), test_scores,  label="Test",  marker='s', markersize=4)

#échelle
y_min = min(min(train_scores), min(test_scores)) - 0.02
y_max = max(max(train_scores), max(test_scores)) + 0.02
ax.set_ylim(y_min, y_max)
ax.grid(True, which='both', linestyle='--', alpha=0.5)
ax.minorticks_on()

ax.set_xlabel("k", fontsize=12)
ax.set_ylabel("Accuracy", fontsize=12)
ax.set_title("Overfitting selon k", fontsize=14)
ax.legend()

plt.tight_layout()
plt.show()
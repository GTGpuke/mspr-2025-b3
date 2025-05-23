import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Chargement des données
df = pd.read_excel("dataset_final.xlsx", sheet_name="Données élections")
df = df[df["résultat élection"].notna()].copy()
df["résultat élection"] = df["résultat élection"].str.lower()

features = [
    "3- Part de retraité (%)",
    "4- Part d'étudiant (%)",
    "6- PIB par habitant (Euros)",
    "7- Taux chomage",
    "9- Part des 24-35 ans diplômés (%)",
    "10- Part de la population en zone rurale (%)"
]
target = "résultat élection"

X = df[features]
y = df[target]

# Encodage cible
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

model_path = "modele_global_rf.joblib"

if os.path.exists(model_path):
    print("Chargement du modèle et encodeur existants...")
    saved_objects = joblib.load(model_path)
    model = saved_objects["model"]
    label_encoder = saved_objects["label_encoder"]
else:
    print("Optimisation et entraînement du modèle Random Forest...")

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [8, 10, 15, None],
        'min_samples_split': [2, 5, 10],
        'class_weight': ['balanced']
    }
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    model = grid_search.best_estimator_
    print(f"Meilleurs hyperparamètres : {grid_search.best_params_}")

    # Sauvegarde modèle + encodeur dans un seul fichier
    joblib.dump({"model": model, "label_encoder": label_encoder}, model_path)
    print("Modèle sauvegardé.")

# Prédiction + évaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nTaux de précision (accuracy) sur le jeu de test : {acc:.2%}")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

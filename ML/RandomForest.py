import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.metrics import classification_report, accuracy_score

# 1. Chargement des données
file_path = "dataset_final.xlsx"  # Adapter au bon chemin
xls = pd.ExcelFile(file_path)
elections_df = xls.parse('Données élections')

# 2. Séparation des données
df_train = elections_df[elections_df["année"] != 2022].copy()
df_predict = elections_df[elections_df["année"] == 2022].copy()

# 3. Préparation des données
df_train = df_train.dropna(subset=["Résultat législative"])
df_train["Résultat législative"] = df_train["Résultat législative"].map({"Droite": 1, "Gauche": 0})

# Colonnes à exclure
excluded_cols = ["année", "région", "résultat élection", "Résultat législative", "Résultat municipale"]
feature_cols = [col for col in df_train.columns if col not in excluded_cols]

# Matrices X et y
X = df_train[feature_cols].fillna(df_train[feature_cols].mean())
y = df_train["Résultat législative"]

# 4. Modèle final Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=2,
    class_weight='balanced',
    random_state=42
)
model.fit(X, y)

# 5. Prédictions pour 2024
X_2024 = df_predict[feature_cols].fillna(X.mean())
regions_2024 = df_predict["région"].values
predictions_2024 = model.predict(X_2024)
proba_2024 = model.predict_proba(X_2024)[:, 1]

# Résultat des prédictions
prediction_df = pd.DataFrame({
    "Région": regions_2024,
    "Prédiction": ["Droite" if p == 1 else "Gauche" for p in predictions_2024],
    "Probabilité Droite": proba_2024
})

print("Prédictions pour les élections 2022 :")
print(prediction_df)

# 6. Évaluation avec validation croisée
print("\n Évaluation du modèle (validation croisée 5-fold) :")
y_pred_cv = cross_val_predict(model, X, y, cv=5)

# Rapport complet
report = classification_report(y, y_pred_cv, target_names=["Gauche", "Droite"], digits=2)
print(report)

# Précision globale
accuracy = accuracy_score(y, y_pred_cv)
print(f"Précision globale : {accuracy:.2f}")
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler
from collections import Counter

# Définition de l’année cible pour la prédiction
ANNEE_CIBLE = 2022

# Liste des variables explicatives utilisées pour la prédiction
features = [
    "3- Part de retraité (%)",
    "4- Part d'étudiant (%)",
    "6- PIB par habitant (Euros)",
    "7- Taux chomage",
    "9- Part des 24-35 ans diplômés (%)",
    "10- Part de la population en zone rurale (%)"
]

# Chargement des données correspondant à l'année ciblée
df = pd.read_excel("dataset_final.xlsx", sheet_name="Données élections")
df = df[df["année"] == ANNEE_CIBLE].copy()

# Vérification de la disponibilité des données pour l’année spécifiée
if df.empty:
    print(f"Aucune donnée trouvée pour l'année {ANNEE_CIBLE}.")
    exit()

# Préparation du label encoder à partir des données historiques contenant les résultats
df_all = pd.read_excel("dataset_final.xlsx", sheet_name="Données élections")
df_all = df_all[df_all["résultat élection"].notna()]
df_all["résultat élection"] = df_all["résultat élection"].str.lower()

label_encoder = LabelEncoder()
label_encoder.fit(df_all["résultat élection"])

# Normalisation des données selon les caractéristiques du jeu d’entraînement
scaler = StandardScaler()
X_all = df_all[features]
scaler.fit(X_all)

# Prétraitement des données de l'année cible
X_predict = df[features]
X_predict_scaled = scaler.transform(X_predict)

# Chargement du modèle entraîné
model = tf.keras.models.load_model("modele_global.h5")

# Génération des prédictions sur les données de l'année cible
y_pred_prob = model.predict(X_predict_scaled).flatten()
y_pred_bin = (y_pred_prob > 0.5).astype(int)
y_pred_labels = label_encoder.inverse_transform(y_pred_bin)

# Agrégation des prédictions pour identifier le camp politique majoritaire
compte = Counter(y_pred_labels)
vainqueur = compte.most_common(1)[0][0]

# Affichage du résultat prédit
print(f"\nPour l'année {ANNEE_CIBLE}, le modèle prédit une victoire de : {vainqueur.upper()}")

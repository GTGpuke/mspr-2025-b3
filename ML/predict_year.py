import pandas as pd
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import joblib
import os

ANNEE_CIBLE = 2007

features = [
    "3- Part de retraité (%)",
    "4- Part d'étudiant (%)",
    "6- PIB par habitant (Euros)",
    "7- Taux chomage",
    "9- Part des 24-35 ans diplômés (%)",
    "10- Part de la population en zone rurale (%)"
]

# Chargement des données pour l'année cible
df = pd.read_excel("dataset_final.xlsx", sheet_name="Données élections")
df = df[df["année"] == ANNEE_CIBLE].copy()

if df.empty:
    print(f"Aucune donnée trouvée pour l'année {ANNEE_CIBLE}.")
    exit()

# Chargement du modèle + label encoder sauvegardés
model_path = "modele_global_rf.joblib"
if not os.path.exists(model_path):
    print(f"Modèle non trouvé à {model_path}. Entraîne-le d'abord.")
    exit()

saved_objects = joblib.load(model_path)
model = saved_objects["model"]
label_encoder = saved_objects["label_encoder"]

# Préparation des features (pas de scaler nécessaire pour Random Forest)
X_predict = df[features]

# Prédiction (classe)
y_pred = model.predict(X_predict)

# Décodage des labels
y_pred_labels = label_encoder.inverse_transform(y_pred)

# Comptage des prédictions
compte = Counter(y_pred_labels)
vainqueur = compte.most_common(1)[0][0]

print(f"\nPour l'année {ANNEE_CIBLE}, le modèle prédit une victoire de : {vainqueur.upper()}")

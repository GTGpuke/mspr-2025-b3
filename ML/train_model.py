import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import os

# Chargement des données à partir du fichier Excel
df = pd.read_excel("dataset_final.xlsx", sheet_name="Données élections")
df = df[df["résultat élection"].notna()].copy()
df["résultat élection"] = df["résultat élection"].str.lower()

# Définition des variables explicatives et de la variable cible
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

# Encodage de la variable cible (catégorique) et normalisation des variables explicatives
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparation du jeu de données en ensemble d'entraînement et de test (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42
)

# Chemin du fichier de sauvegarde du modèle
model_path = "modele_global.h5"

# Définition d’un mécanisme d’arrêt anticipé pour éviter le surapprentissage
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

# Chargement du modèle existant ou création d’un nouveau modèle si absent
if os.path.exists(model_path):
    print("Chargement du modèle existant...")
    model = tf.keras.models.load_model(model_path)
else:
    print("Création d’un nouveau modèle...")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entraînement du modèle avec validation croisée sur 10% du jeu d'entraînement
model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=8,
    validation_split=0.1,
    callbacks=[early_stop]
)

# Prédiction sur les données de test et évaluation des performances
y_pred_prob = model.predict(X_test).flatten()
y_pred = (y_pred_prob > 0.5).astype(int)

acc = accuracy_score(y_test, y_pred)
print(f"\nTaux de précision (accuracy) sur le jeu de test : {acc:.2%}")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Sauvegarde du modèle entraîné
model.save(model_path)
print("Modèle sauvegardé avec succès.")

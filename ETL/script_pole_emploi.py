import pandas as pd
from fuzzywuzzy import process

# 1. Liste officielle des 13 régions
target_regions = [
    "Auvergne-Rhône-Alpes",
    "Bourgogne-Franche-Comté",
    "Bretagne",
    "Centre-Val de Loire",
    "Corse",
    "Grand Est",
    "Hauts-de-France",
    "Normandie",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Pays de la Loire",
    "Provence-Alpes-Côte d’Azur",
    "Île-de-France"
]

# 2. Charger le fichier en précisant que les vrais headers sont à la ligne 7
df = pd.read_excel("D- Demandeurs Pole Emploi de 1996 à 2024.xlsx", header=6)

# 3. Nettoyer : garder colonne A (période) + colonnes des Régions
df = df.rename(columns={df.columns[0]: "Période"})

# 4. Retirer les lignes vides
df = df.dropna(subset=["Période"])

# 5. Extraire l'année à partir de "2002T1"
df["Année"] = df["Période"].astype(str).str.extract(r"(\d{4})").astype(int)

# 6. Filtrer uniquement les années entre 2002 et 2024
df = df[df["Année"].between(2002, 2024)]

# 7. Fuzzy matching pour récupérer uniquement les colonnes des régions demandées
region_columns = list(df.columns[1:-1])  # toutes sauf "Période" et "Année"

def match_region(col_name):
    match, score = process.extractOne(col_name, target_regions)
    return match if score >= 80 else None

matched_columns = {}
for col in region_columns:
    match = match_region(col)
    if match:
        matched_columns[col] = match

# 8. Renommer les colonnes selon les vrais noms des régions
df = df.rename(columns=matched_columns)

# 9. Garder seulement les colonnes correspondant aux régions cibles
df = df[["Année"] + target_regions]

# 10. Faire la moyenne par Année
df_grouped = df.groupby("Année").mean().reset_index()

# 11. Réorganiser : années décroissantes + régions dans l'ordre
df_grouped = df_grouped.sort_values(by="Année", ascending=False)
df_grouped = df_grouped[["Année"] + target_regions]

# 12. Transformer pour avoir Région | Année | Valeur
df_melted = df_grouped.melt(id_vars="Année", var_name="Région", value_name="Demandeurs_Pole_Emploi")

# 13. Trier Région dans l'ordre donné
df_melted["Région"] = pd.Categorical(df_melted["Région"], categories=target_regions, ordered=True)
df_melted = df_melted.sort_values(by=["Année", "Région"])

# 14. Sauvegarder dans un nouveau fichier
df_melted.to_excel("demandeurs_pole_emploi_clean.xlsx", index=False)

print("Fichier 'demandeurs_pole_emploi_clean.xlsx' généré avec succès.")

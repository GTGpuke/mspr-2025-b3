import pandas as pd
from fuzzywuzzy import process

# 1. Charger le fichier
df = pd.read_excel("F- TAUX-CHOMAGE_ans_departement.xlsx")

# 2. Nettoyer la colonne Région (colonne A)
df.iloc[:, 0] = df.iloc[:, 0].str.replace("Taux de chômage localisé par région - ", "").str.strip()

# 3. Liste officielle des 13 régions
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

# 4. Garder uniquement les colonnes utiles
# Colonnes D et suivantes = à partir de l'index 3 (car A=0, B=1, C=2)
trimestre_cols = df.columns[3:]
df = df.iloc[:, [0] + list(range(3, len(df.columns)))]

# 5. Transformer les colonnes trimestre en deux colonnes : Année + Trimestre
df_melted = df.melt(id_vars=[df.columns[0]], value_vars=trimestre_cols, var_name="Trimestre", value_name="Taux_Chomage")

# 6. Extraire l'année à partir de "2002-T1" => 2002
df_melted["Année"] = df_melted["Trimestre"].str.extract(r"(\d{4})").astype(int)

# 7. Grouper par Région + Année pour calculer la moyenne annuelle
df_grouped = df_melted.groupby([df.columns[0], "Année"], as_index=False).mean()

# 8. Fuzzy matching sur les régions pour corriger les petites différences
def match_region(region_name):
    match, score = process.extractOne(region_name, target_regions)
    return match if score >= 80 else None

df_grouped['Région_Match'] = df_grouped[df.columns[0]].apply(match_region)

# 9. Supprimer les lignes sans bonne correspondance
df_grouped = df_grouped.dropna(subset=['Région_Match'])

# 10. Remplacer par le bon nom de région
df_grouped['Région'] = df_grouped['Région_Match']

# 11. Nettoyer
df_grouped = df_grouped[['Région', 'Année', 'Taux_Chomage']]

# 12. Trier les années décroissantes
df_grouped = df_grouped.sort_values(by=["Année"], ascending=False)

# 13. Trier les régions dans ton ordre personnalisé
df_grouped["Région"] = pd.Categorical(df_grouped["Région"], categories=target_regions, ordered=True)
df_grouped = df_grouped.sort_values(by=["Année", "Région"])

# 14. Sauvegarder
df_grouped.to_excel("taux_chomage_region_clean.xlsx", index=False)

print("Fichier 'taux_chomage_region_clean.xlsx' généré avec succès.")

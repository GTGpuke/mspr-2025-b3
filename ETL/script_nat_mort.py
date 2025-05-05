import pandas as pd
from fuzzywuzzy import process

# 1. Charger le fichier Excel avec toutes les feuilles
xls = pd.ExcelFile("A- Evolution situation démographique.xlsx")

# 2. Liste officielle des 13 régions
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

# 3. Fonction pour matcher les régions
def match_region(region_name):
    match, score = process.extractOne(region_name, target_regions)
    return match if score >= 80 else None

# 4. Traiter toutes les feuilles
all_data = []

for sheet_name in xls.sheet_names:

    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    if df.shape[1] < 10:
        continue

    df = df.iloc[:, [0, 8, 9]]
    df.columns = ["Région", "Natalité", "Mortalité"]
    
    df["Région_Match"] = df["Région"].apply(match_region)
    
    df = df.dropna(subset=["Région_Match"])
    
    df["Région"] = df["Région_Match"]
    
    df["Année"] = int(sheet_name)
    
    df = df[["Région", "Année", "Natalité", "Mortalité"]]
    
    all_data.append(df)

# 5. Fusionner toutes les années
final_df = pd.concat(all_data, ignore_index=True)

# 6. Trier par Année décroissante et Région dans l'ordre officiel
final_df = final_df.sort_values(by=["Année"], ascending=False)
final_df["Région"] = pd.Categorical(final_df["Région"], categories=target_regions, ordered=True)
final_df = final_df.sort_values(by=["Année", "Région"])

# 7. Sauvegarder dans un nouveau fichier
final_df.to_excel("evolution_demographique_region_clean.xlsx", index=False)

print("Fichier 'evolution_demographique_region_clean.xlsx' généré avec succès.")

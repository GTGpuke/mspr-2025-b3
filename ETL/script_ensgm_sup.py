import pandas as pd
from fuzzywuzzy import process

# 1. Charger le fichier source
dataset = pd.read_excel("J- Part_25_34_ensgt_sup.xlsx")

# 2. Liste officielle des régions
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

# 3. Garder uniquement les colonnes utiles
dataset = dataset.iloc[:, [1, 2, 3]]
dataset.columns = ["Région", "Année", "Valeur"]

# 4. Trouver pour chaque région du dataset la meilleure correspondance
def match_region(region_name):
    match, score = process.extractOne(region_name, target_regions)
    return match if score >= 80 else None  # 80% de similarité minimum

# 5. Appliquer le matching
dataset['Région_Match'] = dataset['Région'].apply(match_region)

# 6. Supprimer les lignes sans correspondance correcte
dataset = dataset.dropna(subset=['Région_Match'])

# 7. Remplacer par le bon nom de région
dataset['Région'] = dataset['Région_Match']

# 8. Nettoyer
dataset = dataset[["Région", "Année", "Valeur"]]

# 9. Trier par année décroissante
dataset = dataset.sort_values(by=["Année"], ascending=False)

# 10. Trier les régions dans ton ordre personnalisé
dataset["Région"] = pd.Categorical(dataset["Région"], categories=target_regions, ordered=True)
dataset = dataset.sort_values(by=["Année", "Région"])

# 11. Renommer la colonne 'Valeur' pour être plus clair
dataset.rename(columns={"Valeur": "Part_25_34_Enseignement_Supérieur"}, inplace=True)

# 12. Sauvegarder
dataset.to_excel("part_25_34_ensgt_sup_clean_simplefuzzy.xlsx", index=False)

print("Fichier 'part_25_34_ensgt_sup_clean_simplefuzzy.xlsx' généré avec succès.")

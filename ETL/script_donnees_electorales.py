import pandas as pd
from fuzzywuzzy import process

# 1. Charger le fichier Excel
df = pd.read_excel("E- PIB_regionaux_1990-2022.xlsx")

# 2. Renommer les colonnes utiles
df = df.rename(columns={
    df.columns[1]: "Région",
    df.columns[4]: "Abstention",
    df.columns[20]: "Score_Gagnant"
})

# 3. Ne garder que les colonnes d’intérêt
df = df[["Région", "Abstention", "Score_Gagnant"]].dropna()

# 4. Liste officielle des 13 régions métropolitaines
regions_cibles = [
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

# 5. Fuzzy matching pour associer les régions du fichier à la liste officielle
def match_region(nom):
    match, score = process.extractOne(nom, regions_cibles)
    return match if score >= 80 else None

df["Région_Match"] = df["Région"].apply(match_region)

# 6. Supprimer les lignes non reconnues
df = df.dropna(subset=["Région_Match"])

# 7. Remplacer par les bons noms
df["Région"] = df["Région_Match"]
df = df.drop(columns=["Région_Match"])

# 8. Trier dans l’ordre personnalisé
df["Région"] = pd.Categorical(df["Région"], categories=regions_cibles, ordered=True)
df = df.sort_values("Région")

# 9. Exporter le fichier propre
df.to_excel("resultats_electoraux_regionaux.xlsx", index=False)

print("Fichier 'resultats_electoraux_regionaux.xlsx' généré avec succès.")

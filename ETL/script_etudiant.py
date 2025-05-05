import pandas as pd

# Charger le fichier contenant les données brutes
df = pd.read_excel("C- Etudiant en France.xlsx")

# Renommer les colonnes principales (A = Nombre étudiants, C = Région, D = Année)
df.columns = ["Nombre_Etudiants", "?", "Région", "Année"] + list(df.columns[4:])

# Supprimer les lignes incomplètes (par sécurité)
df = df[["Nombre_Etudiants", "Région", "Année"]].dropna()

# S'assurer des bons types
df["Année"] = df["Année"].astype(int)
df["Nombre_Etudiants"] = pd.to_numeric(df["Nombre_Etudiants"], errors="coerce")

# Liste officielle des 13 régions métropolitaines
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

# Filtrer les années et les régions
df = df[df["Année"].between(2002, 2024)]
df = df[df["Région"].isin(regions_cibles)]

# Trier les régions selon l’ordre donné, à l’intérieur de chaque année
df["Région"] = pd.Categorical(df["Région"], categories=regions_cibles, ordered=True)
df = df.sort_values(by=["Année", "Région"], ascending=[False, True])

# Optionnel : grouper par région et année pour obtenir un total par région (si nécessaire)
df = df.groupby(["Année", "Région"], as_index=False).sum()

# Réorganiser les colonnes
df_final = df[["Année", "Région", "Nombre_Etudiants"]]

# Sauvegarder dans un nouveau fichier
df_final.to_excel("etudiants_region_nettoye.xlsx", index=False)

print("Fichier 'etudiants_region_nettoye.xlsx' généré avec succès.")

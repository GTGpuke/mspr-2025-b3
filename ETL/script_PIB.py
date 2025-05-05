import pandas as pd

# 1. Charger les données avec les bons en-têtes
# Ligne 4 contient les noms des années -> donc header=3
df = pd.read_excel("E- PIB_regionaux_1990-2022.xlsx", header=3)

# 2. Liste des régions métropolitaines à conserver (dans l’ordre souhaité)
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

# 3. Garder uniquement les lignes correspondant aux 13 régions métropolitaines
df = df[df.iloc[:, 0].isin(regions_cibles)]

# 4. Transformer les colonnes "année" en lignes (format long)
df_melted = df.melt(id_vars=df.columns[0], var_name="Année", value_name="PIB")
df_melted.columns = ["Région", "Année", "PIB"]

# 5. Nettoyer les types et filtrer uniquement les années 2022 à 2024
df_melted["Année"] = pd.to_numeric(df_melted["Année"], errors="coerce")
# Filtrer les années de 2002 à 2024
df_melted = df_melted[df_melted["Année"].between(2002, 2024)]

# 6. Trier selon ton ordre personnalisé (année décroissante, régions dans l’ordre fixé)
df_melted["Région"] = pd.Categorical(df_melted["Région"], categories=regions_cibles, ordered=True)
df_melted = df_melted.sort_values(by=["Année", "Région"], ascending=[False, True])

# 7. Sauvegarde du résultat dans un fichier propre
df_melted.to_excel("pib_region_restructure.xlsx", index=False)

print("Fichier 'pib_region_restructure.xlsx' généré avec succès.")

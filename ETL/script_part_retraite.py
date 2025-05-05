import pandas as pd

# 1. Charger le fichier source
retraite_dataset = pd.read_excel("B- Part retraités nouvelle région.xlsx")

# 2. Liste des régions à conserver et leur ordre spécifique
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

# 3. Filtrer uniquement les régions d'intérêt
retraite_dataset = retraite_dataset[retraite_dataset["Région"].isin(target_regions)]

# 4. Prendre les colonnes utiles : 'Année', 'Région', et la colonne E
colonne_valeur = retraite_dataset.columns[4]  # colonne E

retraite_dataset = retraite_dataset[["Année", "Région", colonne_valeur]]

# 5. Faire la moyenne s'il existe plusieurs valeurs pour même Année + Région
retraite_dataset = retraite_dataset.groupby(["Année", "Région"], as_index=False).mean()

# 6. Trier les années décroissantes
retraite_dataset = retraite_dataset.sort_values(by=["Année"], ascending=False)

# 7. Remettre les régions dans l'ordre donné pour chaque année
retraite_dataset["Région"] = pd.Categorical(retraite_dataset["Région"], categories=target_regions, ordered=True)
retraite_dataset = retraite_dataset.sort_values(by=["Année", "Région"])

# 8. Renommer la colonne de la valeur si besoin
retraite_dataset.rename(columns={colonne_valeur: "Part_Retraites"}, inplace=True)

# 9. Sauvegarder le fichier propre
retraite_dataset.to_excel("part_retraites_clean.xlsx", index=False)

print("Fichier 'part_retraites_clean.xlsx' généré avec succès.")

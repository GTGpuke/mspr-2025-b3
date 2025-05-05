import pandas as pd


fichiers = [
    "part_retraites_clean.xlsx",
    "pib_region_restructure.xlsx",
    "demandeurs_pole_emploi_clean.xlsx",
    "evolution_demographique_region_clean.xlsx",
    "etudiants_region_nettoye.xlsx",
    "part_25_34_ensgt_sup_clean.xlsx",
    "taux_chomage_region_clean.xlsx",
    "resultats_electoraux_regionaux.xlsx",
]


colonnes = []

for fichier in fichiers:
    df = pd.read_excel(fichier, usecols=[0])
    colonnes.append(df.iloc[:, 0])  


df_concat = pd.concat(colonnes, axis=1)


df_concat.columns = [chr(65 + i) for i in range(len(fichiers))]  

df_concat.to_excel("fusion_colonnes.xlsx", index=False)

print("Fichier 'fusion_colonnes.xlsx' généré avec succès.")

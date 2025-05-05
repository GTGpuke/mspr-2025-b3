import pandas as pd

# 1. Charger le fichier Excel
df = pd.read_excel("nbr_en_part.xlsx")

# 2. Renommer les colonnes 
df.columns = ["Année", "Région", "population", "Nombre d'étudiant", "Part (%)"]

# 3. Calculer la part en pourcentage (Nombre d'étudiant / population) * 100
df["Part (%)"] = (df["Nombre d'étudiant"] / df["population"]) * 100

# 4. Sauvegarder le fichier avec la nouvelle colonne
df.to_excel("population_data_with_part.xlsx", index=False)

print("Fichier 'population_data_with_part.xlsx' généré avec succès.")

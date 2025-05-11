import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le fichier Excel
df = pd.read_excel("dataset_final.xlsx", sheet_name="Données élections")

# Nettoyage de base
df_numeric = df.select_dtypes(include='number').dropna()

# Heatmap de corrélations
plt.figure(figsize=(12, 10))
sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Carte de chaleur des corrélations entre indicateurs")
plt.show()

# Bar plot du taux de chômage par région
plt.figure(figsize=(14, 6))
sns.barplot(data=df, x="région", y="7- Taux chomage", palette="Blues_d")
plt.xticks(rotation=45, ha='right')
plt.title("Taux de chômage par région")
plt.ylabel("Taux de chômage (%)")
plt.xlabel("Région")
plt.tight_layout()
plt.show()

# Scatter plot : PIB par habitant vs Taux de chômage
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="6- PIB par habitant (Euros)", y="7- Taux chomage", hue="région", palette="tab10", s=100)
plt.title("PIB par habitant vs Taux de chômage")
plt.xlabel("PIB par habitant (€)")
plt.ylabel("Taux de chômage (%)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Pairplot pour visualiser les relations croisées
sns.pairplot(df_numeric)
plt.suptitle("Relations croisées entre indicateurs", y=1.02)
plt.show()

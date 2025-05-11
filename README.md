
<h1 align="center"> MSPR</h1>
<h1 align="center"> « Big Data et Analyse de données » </h1>

![alt text](Documents\Images\AI.jpg)

---

## Projet de prédiction électorale avec du machine learning
Ce projet a été réalisé dans le cadre d'un projet scolaire pour créer une preuve de concept (POC) sur la prédiction des tendances électorales en France. Le projet s'appuie sur des jeux de données historiques d'élections, ainsi que sur des indicateurs socio-économiques tels que le taux de chômage et la démographie.

### Objectif du projet

L'objectif de ce projet est de développer un modèle prédictif, basé sur des données historiques, permettant de prédire les résultats des élections futures. 

La POC se concentre sur un secteur géographique restreint et combine des données d'élections présidentielles et législatives, ainsi que des données sur le chômage et la démographie.

### Equipe 

- Combee Nikki
- Dilmamode Yasmine
- Ledeuil Pierre
- Penarrubia Valentin

### Description du contenue du repository

- **Dossier [Datas_Warehouse](Datas_Warehouse/)** :
    - Contient 3 fichiers : 
        - Un fichier python (**[load_datawarehouse.py](Data_Warehouse\load_datawarehouse.py)**) qui lance un script pour initialiser le DW et y insérer les données finales
        - Un script sql (**[script_init_datawarehouse.sql](Data_Warehouse\script_init_datawarehouse.sql)**) pour construire la bdd
        - le dataset final résultant de l'ETL

<br>

- **Dossier [Datas](Datas/)** :
    - Contient les fichiers de données utilisées par notre ETL

<br>

- **Dossier [Documents](Documents/)** :
    - Contient : 
        - Le sujet du projet
        - Un dossier **[Images](Images/)**      
        - Un dossier **[Visualisations](Visualisations/)** contenant : 
            - Un dossier avec les visualisations PowerBi
            - Un dossier avec du code pour une visualisation avec Python

<br>

- **Dossier [ETL](ETL/)** :
    - Contient le code de notre ETL 

<br>

- **Dossier [ML](ML/)** :
    - Contient les fichiers utiliser pour notre Machine Learning
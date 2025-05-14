## Data Warehouse – Projet Électoral & Données Socio-Économiques

#### Objectif
Ce projet construit un data warehouse (schéma en étoile) à partir d’un fichier Excel contenant des données électorales et socio-économiques par région et par année. Il insère les données dans une base MySQL, prête à être analysée.

---

#### Structure du projet

```bash
/Data_Warehouse/
│
├── dataset_final.xlsx               # Fichier source des données (Excel)
├── script_init_datawarehouse.sql   # Script SQL pour créer les tables et la base
├── load_datawarehouse.py           # Script Python d'importation des données
├── README.md                       # Ce fichier
```

---

#### Outils utilisés

- ***MySQL (via WAMP)***

Système de gestion de base de données relationnelle utilisé pour héberger le data warehouse. Installé à travers WAMP.
Les tables sont créées avec le ***moteur InnoDB***, permettant la gestion des clés étrangères et des relations complexes entre les données.

- ***Python 3.x***

Langage de programmation principal utilisé pour automatiser l’importation des données depuis un fichier Excel vers la base MySQL.

Bibliothèques utilisées :

- ***pandas*** : pour lire et manipuler le fichier .xlsx efficacement.

- ***openpyxl*** : pour permettre à pandas de lire les fichiers Excel.

- ***mysql-connector-python*** : pour établir une connexion directe entre Python et le serveur MySQL.

Permet également de charger dynamiquement un fichier ***.sql*** pour initialiser la base de données.

- ***phpMyAdmin (pour visualiser les données)***

Interface web facilitant la gestion et l’exploration de la base MySQL.

Utilisée ici pour :

- Vérifier visuellement les relations entre les tables.

- Exécuter des requêtes SQL manuellement.

- Naviguer facilement dans les dimensions et les données de faits.


<br>

#### Installation les bibliothèques Python nécessaires :

```bash
pip install pandas openpyxl mysql-connector-python
```

---

### Description des scripts et exécution
<br>

##### 1. Le script d'initialisation de la base de données

Le fichier [***script_init_datawarehouse.sql***](script_init_datawarehouse.sql) contient :

- La création de la base de données ***datawarehouse_pres***
<br>
- La création de 3 tables de dimenssion :
    - ***dim_temps***
    - ***dim_region***
    - ***dim_societe***
    <br>
- La création de 3 tables de fait 
    - ***fait_election_presidentielle***
    - ***fait_election_legislative***
    - ***fait_election_municipale***

Les tables possédent des relations de ***clés étrangères*** (avec ***InnoDB***)

Toutes les tables sont liées par des relations typiques d’un schéma en étoile.

<br>

##### 2. Le script Python 

Le script [***load_datawarehouse.py***](load_datawarehouse.py) :

1. Se connecte à MySQL

2. Exécute le script SQL pour créer la base et les tables

3. Lit les données de ***dataset_final.xlsx***

4. Insère chaque ligne dans les tables appropriées

5. Gère les relations via des clés étrangères

<br>

##### 3. Lancer le le script :

Pour que le script fonctionne, il faut que ***Wamp*** soit démarré. 

```bash
# Ouvrir le dossier courant dans un terminal et lancer la commande suivante : 
python load_datawarehouse.py
```

---

#### Visualisation

Utilise phpMyAdmin pour :

- Naviguer dans la base datawarehouse

- Vérifier les relations (onglet Structure > Relation view)

- Effectuer des requêtes analytiques sur la table de faits


La structure actuelle est prête pour des requêtes en étoile avec JOIN.
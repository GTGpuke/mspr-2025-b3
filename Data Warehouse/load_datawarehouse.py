import pandas as pd
import mysql.connector
import os


cursor = None
conn = None

try:
    # Connexion
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()

    # Lire et exécuter ton script SQL
    with open("script_init_datawarehouse.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)

    # Sélectionner la base après création
    cursor.execute("USE datawarehouse_pres")

    print("Data warehouse crée avec succès.")


    # === CHARGER LE FICHIER EXCEL ===
    df = pd.read_excel("dataset_final.xlsx", sheet_name=0)
    df.columns = [col.strip().lower().replace("_", " ") for col in df.columns]
    df.columns = [
        "annee", "region", "resultat_election", "score_gagnant",
        "taux_abstention", "taux_natalite", "taux_mortalite",
        "part_retraite", "part_etudiant", "nbre_demandeur_emploi",
        "pib_habitant", "taux_chomage", "indice_securite",
        "part_diplomes_24_35", "part_zone_rurale", "resultat_legislative", "resultat_municipale"
    ]


    # === INSERTION DES DONNÉES ===
    for i, row in df.iterrows():
        # DIM TEMPS
        cursor.execute("SELECT id_temps FROM dim_temps WHERE annee = %s", (int(row.annee),))
        result = cursor.fetchone()

        if result:
            id_temps = result[0]
        else:
            cursor.execute("INSERT INTO dim_temps (annee) VALUES (%s)", (int(row.annee),))
            id_temps = cursor.lastrowid

        # DIM RÉGION
        cursor.execute("SELECT id_region FROM dim_region WHERE nom_region = %s", (row.region,))
        result = cursor.fetchone()

        if result:
            id_region = result[0]
        else:
            cursor.execute("INSERT INTO dim_region (nom_region) VALUES (%s)", (row.region,))
            id_region = cursor.lastrowid

        # DIM SOCIÉTÉ
        cursor.execute("""
            INSERT INTO dim_societe (
                taux_natalite, taux_mortalite, part_retraite, part_etudiant,
                nbre_demandeur_emploi, pib_habitant, taux_chomage, indice_securite,
                part_diplomes_24_35, part_zone_rurale
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row.taux_natalite, row.taux_mortalite, row.part_retraite, row.part_etudiant,
            row.nbre_demandeur_emploi, row.pib_habitant, row.taux_chomage,
            row.indice_securite, row.part_diplomes_24_35, row.part_zone_rurale
        ))
        id_societe = cursor.lastrowid

        # TABLES DE FAITS

        # Table presidentielle
        if pd.notnull(row.resultat_election) and pd.notnull(row.score_gagnant) and pd.notnull(row.taux_abstention):
            cursor.execute("""
                INSERT INTO fait_election_presidentielle (
                    id_temps, id_region, id_societe,
                    resultat_election, score_gagnant, taux_abstention
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_temps, id_region, id_societe,
                row.resultat_election, row.score_gagnant, row.taux_abstention
            ))

        # Table legislative
        if pd.notnull(row.resultat_legislative):
            cursor.execute("""
                INSERT INTO fait_election_legislative (
                    id_temps, id_region, id_societe,
                    resultat
                ) VALUES (%s, %s, %s, %s)
            """, (
                id_temps, id_region, id_societe,
                row.resultat_legislative
            ))

        # Table municipale
        if pd.notnull(row.resultat_municipale):
            cursor.execute("""
                INSERT INTO fait_election_municipale (
                    id_temps, id_region, id_societe,
                    resultat
                ) VALUES (%s, %s, %s, %s)
            """, (
                id_temps, id_region, id_societe,
                row.resultat_municipale
            ))
        


    print("Data warehouse charger avec succès.")    

    # === COMMIT & FERMETURE ===
    conn.commit()

# Lever d'exeption si cela échoue
except mysql.connector.Error as err:
    print("==> Erreur SQL :", err)

# FERMETURE 

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("Data warehouse crée et charger avec succès")




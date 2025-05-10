DROP DATABASE IF EXISTS datawarehouse_pres;

CREATE DATABASE IF NOT EXISTS datawarehouse_pres;
USE datawarehouse_pres;

-- TABLE DE DIMENSION : TEMPS
DROP TABLE IF EXISTS dim_temps;
CREATE TABLE dim_temps (
    id_temps INT AUTO_INCREMENT PRIMARY KEY,
    annee INT
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- TABLE DE DIMENSION : RÉGION
DROP TABLE IF EXISTS dim_region;
CREATE TABLE dim_region (
    id_region INT AUTO_INCREMENT PRIMARY KEY,
    nom_region VARCHAR(100)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- TABLE DE DIMENSION : SOCIÉTÉ / INDICATEURS
DROP TABLE IF EXISTS dim_societe;
CREATE TABLE dim_societe (
    id_societe INT AUTO_INCREMENT PRIMARY KEY,
    taux_natalite FLOAT,
    taux_mortalite FLOAT,
    part_retraite FLOAT,
    part_etudiant FLOAT,
    nbre_demandeur_emploi INT,
    pib_habitant FLOAT,
    taux_chomage FLOAT,
    indice_securite FLOAT,
    part_diplomes_24_35 FLOAT,
    part_zone_rurale FLOAT
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- TABLE DE FAITS : RÉSULTATS DES ÉLECTIONS
DROP TABLE IF EXISTS fait_election_regionale;
CREATE TABLE fait_election_regionale (
    id_fait INT AUTO_INCREMENT PRIMARY KEY,
    id_temps INT,
    id_region INT,
    id_societe INT,
    resultat_election VARCHAR(100),
    score_gagnant FLOAT,
    taux_abstention FLOAT,
    FOREIGN KEY (id_temps) REFERENCES dim_temps(id_temps),
    FOREIGN KEY (id_region) REFERENCES dim_region(id_region),
    FOREIGN KEY (id_societe) REFERENCES dim_societe(id_societe)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
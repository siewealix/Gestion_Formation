from db import connexion_bd

def creer_tables():
    connexion = connexion_bd()
    curseur = connexion.cursor()

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS etudiants (
        ine_etudiant TEXT PRIMARY KEY,
        nom_etudiant TEXT NOT NULL,
        prenom_etudiant TEXT NOT NULL,
        email_etudiant TEXT NOT NULL,
        adresse_etudiant TEXT,
        ville_etudiant TEXT
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS formations (
        code_formation TEXT PRIMARY KEY,
        intitule_formation TEXT NOT NULL,
        langue_formation TEXT NOT NULL,
        niveau_formation TEXT NOT NULL,
        objectif_formation TEXT
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS inscription (
        id_inscription INTEGER PRIMARY KEY AUTOINCREMENT,
        ine_etudiant TEXT NOT NULL,
        code_formation TEXT NOT NULL,
        date_inscription TEXT NOT NULL,
        FOREIGN KEY (ine_etudiant) REFERENCES etudiants(ine_etudiant),
        FOREIGN KEY (code_formation) REFERENCES formations(code_formation)
    )
    """)

    connexion.commit()
    connexion.close()
    print("Base de données créée avec succès.")

if __name__ == "__main__":
    creer_tables()
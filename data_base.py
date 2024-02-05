import sqlite3


def creer_base_de_donnees(nom_base_de_donnees, nom_table, colonnes):
    # Connexion à la base de données (le fichier sera créé s'il n'existe pas)
    conn = sqlite3.connect(nom_base_de_donnees)

    # Création d'un objet curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()

    # Création de la table
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {nom_table} (
            {', '.join(colonnes)}
        )
    '''
    cursor.execute(create_table_query)

    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()


def inserer_donnees(nom_base_de_donnees, nom_table, donnees):
    # Connexion à la base de données
    conn = sqlite3.connect(nom_base_de_donnees)

    # Création d'un objet curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()

    # Insertion des données
    insert_query = f'INSERT INTO {nom_table} VALUES ({", ".join(["?" for _ in donnees])})'
    cursor.execute(insert_query, donnees)

    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()


def recuperer_donnees(nom_base_de_donnees, nom_table):
    # Connexion à la base de données
    conn = sqlite3.connect(nom_base_de_donnees)

    # Création d'un objet curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()

    # Récupération de toutes les données de la table
    select_query = f'SELECT * FROM {nom_table}'
    cursor.execute(select_query)

    # Récupération des résultats
    resultats = cursor.fetchall()

    # Fermeture de la connexion
    conn.close()

    return resultats


def delete_table(nom_base_de_donnees, nom_table):
    # Connexion à la base de données
    conn = sqlite3.connect(nom_base_de_donnees)

    # Création d'un objet curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()

    # Suppression de la table
    delete_table_query = f'DROP TABLE {nom_table}'
    cursor.execute(delete_table_query)

    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()
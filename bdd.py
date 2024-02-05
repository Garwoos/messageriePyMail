import sqlite3

# Création de la base de données SQLite
conn = sqlite3.connect('bdd.db')
cursor = conn.cursor()

# Création de la table "users"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        iduser INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        admin INTEGER NOT NULL
    )
''')

# Création de la table "groups"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        idgroup INTEGER PRIMARY KEY,
        group_name TEXT NOT NULL
    )
''')

# Création de la table "user_groups"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_groups (
        iduser INTEGER,
        idgroup INTEGER,
        message TEXT,
        PRIMARY KEY (iduser, idgroup),
        FOREIGN KEY (iduser) REFERENCES users(iduser),
        FOREIGN KEY (idgroup) REFERENCES groups(idgroup)
    )
''')

# Enregistrement des modifications
conn.commit()

# Fermeture de la connexion
conn.close()

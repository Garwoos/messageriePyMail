import sqlite3

# Création de la base de données SQLite
conn = sqlite3.connect('bdd.db')
cursor = conn.cursor()

def add_user(iduser, username, password, admin):
    """
    Ajoute un utilisateur à la base de données.

    Parameters:
        iduser (int): L'identifiant de l'utilisateur.
        username (str): Le nom d'utilisateur.
        password (str): Le mot de passe.
        admin (int): Le statut d'administrateur.
    """
    cursor.execute('''
        INSERT INTO users (iduser, username, password, admin)
        VALUES (?, ?, ?, ?)
    ''', (iduser, username, password, admin))

    conn.commit()

def add_group(idgroup, group_name):
    """
    Ajoute un groupe à la base de données.

    Parameters:
        idgroup (int): L'identifiant du groupe.
        group_name (str): Le nom du groupe.
    """
    cursor.execute('''
        INSERT INTO groups (idgroup, group_name)
        VALUES (?, ?)
    ''', (idgroup, group_name))

    conn.commit()

def add_user_group(iduser, idgroup, message):
    """
    Ajoute un utilisateur à un groupe.

    Parameters:
        iduser (int): L'identifiant de l'utilisateur.
        idgroup (int): L'identifiant du groupe.
        message (str): Le message.
    """
    cursor.execute('''
        INSERT INTO user_groups (iduser, idgroup, message)
        VALUES (?, ?, ?)
    ''', (iduser, idgroup, message))

    conn.commit()

def get_user_groups(iduser):
    """
    Récupère les groupes d'un utilisateur.

    Parameters:
        iduser (int): L'identifiant de l'utilisateur.

    Returns:
        list: La liste des groupes de l'utilisateur.
    """
    cursor.execute('''
        SELECT idgroup, group_name
        FROM groups
        WHERE idgroup IN (
            SELECT idgroup
            FROM user_groups
            WHERE iduser = ?
        )
    ''', (iduser,))

    return cursor.fetchall()

def get_users():
    """
    Récupère les utilisateurs.

    Returns:
        list: La liste des utilisateurs.
    """
    cursor.execute('''
        SELECT iduser, username, admin
        FROM users
    ''')

    return cursor.fetchall()

def get_user(iduser):
    """
    Récupère un utilisateur.

    Parameters:
        iduser (int): L'identifiant de l'utilisateur.

    Returns:
        tuple: L'utilisateur.
    """
    cursor.execute('''
        SELECT iduser, username, password, admin
        FROM users
        WHERE iduser = ?
    ''', (iduser,))

    return cursor.fetchone()

def get_group(idgroup):
    """
    Récupère un groupe.

    Parameters:
        idgroup (int): L'identifiant du groupe.

    Returns:
        tuple: Le groupe.
    """
    cursor.execute('''
        SELECT idgroup, group_name
        FROM groups
        WHERE idgroup = ?
    ''', (idgroup,))

    return cursor.fetchone()

def get_user_group(iduser, idgroup):
    """
    Récupère un utilisateur dans un groupe.

    Parameters:
        iduser (int): L'identifiant de l'utilisateur.
        idgroup (int): L'identifiant du groupe.

    Returns:
        tuple: L'utilisateur dans le groupe.
    """
    cursor.execute('''
        SELECT iduser, idgroup, message
        FROM user_groups
        WHERE iduser = ? AND idgroup = ?
    ''', (iduser, idgroup))

    return cursor.fetchone()
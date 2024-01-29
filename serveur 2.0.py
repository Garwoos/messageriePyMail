from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
import threading
import json
import os


class Server:
    def __init__(self):
        self.host = ""
        self.port = 5555
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(100)
        self.clients = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.close()


# Fonction pour gérer chaque client
def handle_client(client_socket):
    while True:
        # Recevoir le message du client
        message = client_socket.recv(1024).decode('utf-8')

        if not message:
            break

        print(f'Message reçu: {message}')

    client_socket.close()


# Fonction pour créer un nouveau compte

def create_account(username, password):
    try:
        if not os.path.exists('users.json'):
            with open('users.json', 'w') as users_file:
                json.dump({}, users_file)

        with open('users.json', 'r') as users_file:
            users = json.load(users_file)

    except json.JSONDecodeError:
        print("Erreur : Le fichier 'users.json' est mal formé.")
        return False

    except OSError:
        print("Erreur : Impossible d'ouvrir le fichier 'users.json'.")
        return False

    if username in users:
        return False

    users[username] = password

    try:
        with open('users.json', 'w') as users_file:
            json.dump(users, users_file)

    except OSError:
        print("Erreur : Impossible d'écrire dans le fichier 'users.json'.")
        return False

    return True


def main():
    with Server() as server:
        while True:
            # Accepter une connexion du client
            client_socket, addr = server.server.accept()
            print(f'Connexion établie avec {addr}')

            # Lire le message du client
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Message reçu: {message}')


if __name__ == "__main__":
    main()

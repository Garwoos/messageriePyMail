from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread
import random
import logging
import json
import hashlib

class Server:
    """
    This class represents a TCP server.
    """
    def __init__(self):
        self.host = ""
        self.port = 5555
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.clients = {}
        self.identifiers = {}
        self.setup_logging()
        self.users = self.load_users()

    def setup_logging(self):
        # Configurer le niveau de logging global
        logging.basicConfig(level=logging.DEBUG)

        # Créer un logger pour le serveur
        self.server_logger = logging.getLogger('server_logger')
        self.server_logger.setLevel(logging.INFO)  # Niveau de logging pour le serveur

        # Créer un gestionnaire de fichiers pour le serveur
        server_file_handler = logging.FileHandler('server_logs.log')
        server_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        server_file_handler.setFormatter(server_formatter)
        self.server_logger.addHandler(server_file_handler)

    def log_server_info(self, message):
        self.server_logger.info(message)

    def start_server(self):
        self.server.listen(15)
        self.log_server_info("Server started and waiting for connections.")
        while True:
            client, addr = self.server.accept()
            self.log_server_info(f'New client connected: {addr}')
            if addr in self.clients:
                old_client = self.clients[addr]
                old_client.close()
            self.clients[addr] = client
            self.display_clients()
            Thread(target=self.single_client, args=(client, addr)).start()


    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        return users
    

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)


    def register_user(self, username, password):
        self.users[username] = self.hash_password(password)
        self.save_users()

    def generate_identifier(self, client, addr):
        identifier = None
        while not identifier or identifier in self.clients.keys():
            identifier = client.recv(1024).decode('utf-8') + '#'
            for i in range(4):
                identifier += f"{random.randint(0, 9)}"
        self.clients[identifier] = client
        self.identifiers[addr] = identifier
        self.log_server_info(f"{identifier} has connected.")
        return identifier


    def handle_client_messages(self, client, identifier):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                self.log_server_info(f'Message from {identifier}: {message}')
                self.send_message_to_all_except_sender(identifier, message)
            except ConnectionResetError:
                self.log_server_info(f"Failed to receive message from {identifier}. "
                                     "Error: [WinError 10054] An existing connection was forcibly closed by the remote host")
                break


    def send_message_to_all_except_sender(self, sender_identifier, message):
        for identifier, client in self.clients.items():
            if identifier != sender_identifier:
                client.send((f"{sender_identifier}: {message}").encode('utf-8'))



    def send_message_to_specific_client(self):
        identifier = input("Enter the identifier of the client to send a message to: ")
        message = input("Enter the message to send: ")
        self.send_message_to_client(identifier, message)

    def single_client(self, client, addr):
        """
        This function handles a single client connection.
        """
        identifier = None
        try:
            identifier = self.generate_identifier(client, addr)
            self.handle_client_messages(client, identifier)
        except ConnectionResetError:
            if identifier:
                print(f"{identifier} disconnected unexpectedly.\n")
            else:
                print(f"Client at {addr} disconnected unexpectedly.\n")
        finally:
            self.disconnect_client(addr)


    def send_message(self, message):
        """
        This method sends a message to all connected clients.
        """
        for identifier in self.clients:
            self.clients[identifier].send(message.encode('utf-8'))

    def send_message_to_client(self, identifier, message):
        """
        This method sends a message to a specific client.
        """
        if identifier in self.clients:
            self.clients[identifier].send(message.encode('utf-8'))
        else:
            print(f"No client with identifier {identifier}")


    def disconnect_client(self, addr):
        identifier = self.identifiers[addr]
        self.log_server_info(f'{identifier} has disconnected.')
        self.send_message(f"Client {identifier} has disconnected.")
        del self.clients[identifier]
        del self.identifiers[addr]
        self.display_clients()


    def display_clients(self):
        self.log_server_info("Connected clients:")
        for addr in self.clients:
            self.log_server_info(f'Client at {addr}')


    def send_message_prompt(self):
        choice = input("Do you want to send a message to a specific client or to all clients? (Enter 'specific' or 'all'): ")
        if choice.lower() == 'specific':
            self.send_message_to_specific_client()
        elif choice.lower() == 'all':
            message = input("Enter the message to send: ")
            self.send_message(message)
        else:
            self.log_server_info("Invalid choice. Please enter 'specific' or 'all'.")
 


if __name__ == "__main__":
    server = Server()
    server.start_server()
    while True:
        server.send_message_prompt()
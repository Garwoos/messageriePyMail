from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread
import random
import string
import logging
import json
import hashlib

class Server:
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.server.close()

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG)

        self.server_logger = logging.getLogger('server_logger')
        self.server_logger.setLevel(logging.INFO)

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
            client.send("You are now connected to the server.".encode('utf-8'))  # Send connection confirmation to client
            if addr in self.clients:
                old_client = self.clients[addr]
                old_client.close()
            self.clients[addr] = client
            self.display_clients()
            Thread(target=self.single_client, args=(client, addr)).start()

    def load_users(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_users(self):
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(self.users, f)

    def register_user(self, username, password):
        self.users[username] = self.hash_password(password)
        self.save_users()

    def check_password(self, username, password):
        if username in self.users:
            return self.users[username] == self.hash_password(password)
        print(f"Utilisateur '{username}' non trouvé.")
        return False

    def generate_identifier(self, client, addr):
        users = self.load_users()
        identifier = None
        while not identifier or identifier in self.clients:
            identifier = random.choice(list(users.keys())) + '#'
            for _ in range(4):
                identifier += random.choice(string.ascii_letters + string.digits)
        return identifier

    def handle_client_messages(self, client, identifier):
            while True:
                try:
                    message = client.recv(1024).decode('utf-8')
                    if not message:
                        break
                    if message.startswith("LOGIN "):
                        username, password = message.split(" ")[1:]
                        if self.check_password(username, password):
                            self.send_message_to_client(identifier, "Login successful.")
                        else:
                            self.send_message_to_client(identifier, "Login failed.")
                    elif message.startswith("REGISTER "):
                        username, password = message.split(" ")[1:]
                        self.register_user(username, password)
                        self.send_message_to_client(identifier, "Registration successful.")
                    else:
                        self.log_server_info(f'Message from {identifier}: {message}')
                        self.send_message_to_all_except_sender(identifier, message)
                except ConnectionResetError:
                    self.log_server_info(f"Failed to receive message from {identifier}. "
                                        "Error: [WinError 10054] An existing connection was forcibly closed by the remote host")
                    break
                
    def send_message_to_all_except_sender(self, sender_identifier, message):
        [client.send(f"{sender_identifier}: {message}".encode('utf-8')) for identifier, client in self.clients.items() if identifier != sender_identifier]

    def send_message_to_specific_client(self):
        identifier = input("Enter the identifier of the client to send a message to: ")
        message = input("Enter the message to send: ")
        self.send_message_to_client(identifier, message)

    def single_client(self, client, addr):
        identifier = self.generate_identifier(client, addr)
        self.send_message_to_client(identifier, "Do you want to (l)ogin or (r)egister?")
        try:
            self.handle_client_messages(client, identifier)
        except ConnectionResetError:
            if identifier:
                print(f"{identifier} disconnected unexpectedly.\n")
            else:
                print(f"Client at {addr} disconnected unexpectedly.\n")
        finally:
            self.disconnect_client(addr)


    def send_message(self, message):
        for identifier, client in self.clients.items():
            try:
                client.send(message.encode('utf-8'))
            except ConnectionResetError:
                self.log_server_info(f"Failed to send message to {identifier}. "
                                    "Error: [WinError 10054] An existing connection was forcibly closed by the remote host")

    def send_message_to_client(self, identifier, message):
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
            
if __name__ == "__main__":
    with Server() as server:
        server.start_server()
        while True:
            server.send_message_prompt()

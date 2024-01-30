from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
import threading
import json
import os
from datetime import datetime


class Server:
    """
    This class represents a server that can accept connections from clients.

    Attributes:
    host (str): The host on which the server is running.
    port (int): The port on which the server is listening.
    server (socket): The socket object representing the server.
    clients (dict): A dictionary to store connected clients.
    """

    def __init__(self):
        """
        The constructor for Server class. Initializes the server socket and starts listening for connections.
        """
        self.host = ""
        self.port = 5555
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(100)
        self.clients = {}
        self.version = "1.0"

    def __enter__(self):
        """
        Makes Server class compatible with 'with' statement. Returns the server instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures the server socket is closed when exiting a 'with' statement.
        """
        self.server.close()

    def start_server(self):
        """
        Starts the server and accepts connections from clients.

        Parameters:
        host (str): The host on which the server is running.
        port (int): The port on which the server is listening.
        """
        while True:
            # Accept a connection from the client
            client_socket, addr = self.server.accept()
            print(f'Connection established with {addr}')

            # Create a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

def check_version(self, version_user):
    """
    Function to check if the client version is compatible with the server version.

    Parameters:
    version (str): The version of the client.

    Returns:
    bool: True if the client version is compatible with the server version, False otherwise.
    """
    if self.version == version_user :
        return True
    else:
        return False
# Function to handle each client
def handle_client(client_socket):
    """
    Function to handle communication with a client. Receives messages from the client and prints them.

    Parameters:
    client_socket (socket): The socket object representing the client connection.
    """
    while True:
        # Receive the message from the client
        message = client_socket.recv(1024).decode('utf-8')

        if not message:
            break

        print(f'Message received: {message}')

    client_socket.close()


# Function to store every ip address and port number of the clients connected to the server
def store_ipaddr_portnum_connected(addr):
    """
    Function to store the IP address and port number of each client connected to the server in a JSON file.

    Parameters:
    addr (tuple): The IP address and port number of the client.

    Returns:
    bool: True if the IP address and port number were stored successfully, False otherwise.
    """
    # Initialiser ipconnected en chargeant le fichier JSON s'il existe
    if os.path.exists('ipconnected.json'):
        try:
            with open('ipconnected.json', 'r') as ipconnected_file:
                ipconnected = json.load(ipconnected_file)
        except json.JSONDecodeError:
            print("Warning: The 'ipconnected.json' file is malformed. Resetting to an empty dictionary.")
            ipconnected = {}
    else:
        ipconnected = {}

    ip, port = addr  # Décomposer l'adresse en IP et port

    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Si l'IP existe déjà, ajouter les nouvelles informations à la liste existante
    # Sinon, créer une nouvelle liste pour cette IP
    if ip in ipconnected:
        ipconnected[ip].append({"port": port, "timestamp": timestamp})
    else:
        ipconnected[ip] = [{"port": port, "timestamp": timestamp}]

    try:
        with open('ipconnected.json', 'w') as ipconnected_file:
            json.dump(ipconnected, ipconnected_file)

    except Exception as e:
        print("Error: Unable to write to the 'ipconnected.json' file.")
        return False

    return True

def store_message_user(message, username):
    """
    Function to store the messages sent by each user in a JSON file.

    Parameters:
    message (str): The message sent by the user.
    username (str): The username of the user.

    Returns:
    bool: True if the message was stored successfully, False otherwise.
    """
    if os.path.exists('message_user.json'):
        try:
            with open('message_user.json', 'r') as file:
                message_user_dict = json.load(file)
        except json.JSONDecodeError:
            print("Warning: The 'message_user.json' file is malformed. Resetting to an empty dictionary.")
            message_user_dict = {}
    else:
        message_user_dict = {}

    current_time = datetime.now().strftime('%Y-%m-%d.%H:%M:%S')  # Get the current time with reduced precision

    if username in message_user_dict:
        message_user_dict[username].append({"message": message, "time": current_time})
    else:
        message_user_dict[username] = [{"message": message, "time": current_time}]

    try:
        with open('message_user.json', 'w') as file:
            json.dump(message_user_dict, file)
    except Exception as e:
        print(f"Error: Unable to write to the 'message_user.json' file. Error details: {str(e)}")
        return False

    return True


# Function to create a new account
def register(username, password):
    """
    Function to create a new account. Stores the username and password in a JSON file.

    Parameters:
    username (str): The username for the new account.
    password (str): The password for the new account.

    Returns:
    bool: True if the account was created successfully, False otherwise.
    """
    try:
        if not os.path.exists('users.json'):
            with open('users.json', 'w') as users_file:
                json.dump({}, users_file)

        with open('users.json', 'r') as users_file:
            users = json.load(users_file)

    except json.JSONDecodeError:
        print("Warning : The 'users.json' file is malformed. Resetting to an empty dictionary.")
        users = {}



    except OSError:
        print("Error: Unable to open the 'users.json' file.")
        return False

    if username in users:
        print(f"This username already exists. Please try username.")
        return False

    time = datetime.now().strftime('%Y-%m-%d.%H:%M:%S')  # Get the current time with reduced precision
    users[username] = {"password": password, "time": time}


    try:
        with open('users.json', 'w') as users_file:
            json.dump(users, users_file)

    except OSError:
        print("Error: Unable to write to the 'users.json' file.")
        return False

    return True

def login(username, password):
    """
    Function to log in to an existing account. Checks if the username and password match.

    Parameters:
    username (str): The username for the account.
    password (str): The password for the account.

    Returns:
    bool: True if the login was successful, False otherwise.
    """
    try:
        with open('users.json', 'r') as users_file:
            users = json.load(users_file)

    except json.JSONDecodeError:
        print("Error: The 'users.json' file is malformed.")
        return False

    except OSError:
        print("Error: Unable to open the 'users.json' file.")
        return False

    if username not in users or users[username] != password:
        return False

    return True



def main():
    """
    The main function that starts the server and accepts connections from clients.
    """
    with Server() as server:
        while True:
            if True:
                register("test", "password")
            # Accept a connection from the client
            client_socket, addr = server.server.accept()
            print(f'Connection established with {addr}')
            store_ipaddr_portnum_connected(addr)
            # Read the message from the client
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Message received: {message}')



if __name__ == "__main__":
    """
    The entry point for the script. Calls the main function.
    """
    main()

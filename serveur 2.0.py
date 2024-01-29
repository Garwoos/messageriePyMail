from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
import threading
import json
import os


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


# Function to create a new account
def create_account(username, password):
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
        print("Error: The 'users.json' file is malformed.")
        return False

    except OSError:
        print("Error: Unable to open the 'users.json' file.")
        return False

    if username in users:
        return False

    users[username] = password

    try:
        with open('users.json', 'w') as users_file:
            json.dump(users, users_file)

    except OSError:
        print("Error: Unable to write to the 'users.json' file.")
        return False

    return True


def main():
    """
    The main function that starts the server and accepts connections from clients.
    """
    with Server() as server:
        while True:
            # Accept a connection from the client
            client_socket, addr = server.server.accept()
            print(f'Connection established with {addr}')

            # Read the message from the client
            message = client_socket.recv(1024).decode('utf-8')
            print(f'Message received: {message}')


if __name__ == "__main__":
    """
    The entry point for the script. Calls the main function.
    """
    main()

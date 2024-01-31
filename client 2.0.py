from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket, error
import threading


class Client:
    """
    This class is responsible for the client's connection to the server.

    Attributes:
        host (str): The server's IP address.
        port (int): The server's port.
        identifier (str): The client's identifier.
        client (socket): The client's socket.

    Methods:
        connect_to_server: Connects the client to the server.
        send_message: Sends a message to the server.
        receive_message: Receives a message from the server.
    """

    def __init__(self, host='localhost', port=5555):
        """
        The constructor for Client class.

        Parameters:
            host (str): The server's IP address.
            port (int): The server's port.
            identifier (str): The client's identifier.
        """
        self.host = host
        self.port = port
        self.username = None
        self.client = socket(AF_INET, SOCK_STREAM)

    def connect_to_server(self):
        """
        Connects the client to the server.
        """
        try:
            self.client.connect((self.host, self.port))
            print(f'Connected to server {self.host}:{self.port}')
        except error as e:
            print(f'Failed to connect to server {self.host}:{self.port}. Error: {e}')

    def login(self, username, password):
        """
        Logs the client in.
        """
        data = f"{self.host}&_&&--@\&{self.port}&&_&&--\&login&_&&--@\&{username}&_&&--@\&{password}"
        try:
            self.client.sendall(data.encode('utf-8'))
            self.username = username
        except error as e:
            print(f'Failed to send message. Error: {e}')

    def register(self, username, password):
        """
        Registers the client.
        """
        data = f"{self.host}&_&&--@\&{self.port}&&_&&--\&register&_&&--@\&{username}&_&&--@\&{password}"
        try:
            self.client.sendall(data.encode('utf-8'))
            self.username = username
        except error as e:
            print(f'Failed to send message. Error: {e}')

    def send_message_to_group(self, message, group_name):
        """
        Sends a message to a group of clients.

        Parameters:
            message (str): The message to send.
        """
        data = f"{self.host}{self.port}&_&&--\&send_message&_&&--@\&{message}&_&&--@\&{group_name}"
        try:
            self.client.sendall(data.encode('utf-8'))

        except error as e:
            print(f'Failed to send message. Error: {e}')

    def create_group(self, group_name):
        """
        Sends a message to a group of clients.

        Parameters:
            message (str): The message to send.
        """
        data = f"{self.host}&_&&--@\&{self.port}&_&&--@\&{group_name}"
        try:
            self.client.sendall(data.encode('utf-8'))

        except error as e:
            print(f'Failed to send message. Error: {e}')



if __name__ == '__main__':
    client = Client()
    client.connect_to_server()
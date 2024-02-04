from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket, error
import threading
import time


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
        self.version = "1.0"

    def connect_to_server(self):
        """
        Connects the client to the server.
        """
        try:
            self.client.connect((self.host, self.port))
            print(f'Connected to server {self.host}:{self.port}')
        except error as e:
            print(f'Failed to connect to server {self.host}:{self.port}. Error: {e}')

    def send_version(self):
        """
        Sends the client's version to the server.
        """
        try:
            self.client.sendall(f"{self.version}".encode('utf-8'))
        except error as e:
            print(f'Failed to send message. Error: {e}')

    def login(self, username, password):
        """
        Logs the client in.
        """
        data = f"{self.host}&{self.port}&_&&--@\&login&_&&--@\&{username}&_&&--@\&{password}"
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

    def get_new_messages(self):
        """
        Receives new messages from the server.
        """
        while True:
            message = self.receive_message()
            if message:
                print(message)

    def receive_message(self):
        """
        Receives a message from the server.
        """
        try:
            return self.client.recv(1024).decode('utf-8')
        except error as e:
            print(f'Failed to receive message. Error: {e}')

    def start_receiving_messages(self):
        """
        Starts receiving messages from the server.
        """
        thread = threading.Thread(target=self.get_new_messages, daemon=True)
        thread.start()

    def disconnect(self):
        """
        Disconnects the client from the server.
        """
        self.client.close()

    def login_or_register(self):
        action = input("Do you want to (l)ogin or (r)egister? ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if action.lower() == 'l':
            self.login(username, password)
        elif action.lower() == 'r':
            self.register(username, password)
        else:
            print("Invalid choice. Please enter 'l' or 'r'.")

    def main(self):
        self.connect_to_server()
        self.send_version()
        time.sleep(0.5)
        self.login_or_register()
        self.start_receiving_messages()

        # Add a small delay or synchronization point here
        # to ensure that the server has processed the version and login messages
        time.sleep(1)

        while True:
            message = input("Enter a message:")
            self.send_message_to_group(message, "group1")
            if message.lower() == 'exit':
                self.disconnect()
                break


if __name__ == '__main__':
    client = Client()
    client.main()

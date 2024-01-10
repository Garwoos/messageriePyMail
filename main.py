"""
This module contains a Server class for handling TCP connections.
"""

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread

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

    def start_server(self):
        """
        This method starts the server.
        """
        self.server.listen(15)  #the maximum queued connections
        print("Waiting for connection...")
        while True:
            client, addr = self.server.accept()
            print(f'A client has connected {addr}')
            Thread(target=single_client, args=(client,)).start()

    def public_method(self):
        """
        This is a public method of the Server class.
        """
        # Your code here

def incoming_connections(server):
    """
    This function handles incoming connections.
    """
    while True:
        client, addr = server.accept()
        print(f'A client has connected {addr}')
        Thread(target=single_client).start()

def single_client(client):
    """
    This function handles a single client connection.
    """
    while True:
        message = client.recv(1024).decode('utf-8')
        if not message:
            break
        print(f'Message from client: {message}')
        
        response = "Message received by the server."
        client.send(response.encode('utf-8'))

if __name__ == "__main__":
    server = Server()
    server.start_server()
    clients = {}

    HOST = '127.0.0.1'
    PORT = 33336
    BUFFERSIZE = 1024
    ADDR = (HOST, PORT)
    EXIT_CMD = "exit()"
    NAME_CMD = "name()"
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SERVER.bind(ADDR)

    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=incoming_connections, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


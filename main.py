from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
from threading import Thread
import random

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

    def start_server(self):
        """
        This method starts the server.
        """
        self.server.listen(15)  # the maximum queued connections
        print("Waiting for connection...\n")
        while True:
            client, addr = self.server.accept()
            print(f'A client has connected {addr}\n')
            self.clients[addr] = client  # Add the client to the clients dictionary
            self.display_clients()  # Display the updated list of clients
            Thread(target=self.single_client, args=(client, addr)).start()  # Pass the address to single_client

    def single_client(self, client, addr):
        """
        This function handles a single client connection.
        """
        identifier = None  # Initialize identifier to None
        try:
            identifier = client.recv(1024).decode('utf-8') + '#'  # Receive the first message as the identifier
            for i in range(4):  # Generate a 4-digit number
                identifier += f"{random.randint(0,9)}"  
            self.clients[addr] = identifier  # Store the identifier in the clients dictionary
            print(identifier + " has connected\n")
            while True:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f'Message from {identifier}: {message}')
                
                response = "Message received by the server.\n"
                client.send(response.encode('utf-8'))
        except ConnectionResetError:
            if identifier:
                print(f"{identifier} disconnected unexpectedly.\n")
            else:
                print(f"Client at {addr} disconnected unexpectedly.\n")
        finally:
            self.disconnect_client(addr)  # Disconnect the client when it's done


    def send_message(self, message):
        """
        This method sends a message to all connected clients.
        """
        for addr in self.clients:
            self.clients[addr].send(message.encode('utf-8'))

    def send_message_to_client(self, addr, message):
        """
        This method sends a message to a specific client.
        """
        if addr in self.clients:
            self.clients[addr].send(message.encode('utf-8'))
        else:
            print(f"No client at address {addr}")

    def disconnect_client(self, addr):
        """
        This method disconnects a client and updates the list of clients.
        """
        print(f'\nClient at {addr} has disconnected')  # Display the address of the disconnected client
        del self.clients[addr]  # Remove the client from the clients dictionary
        self.display_clients()  # Display the updated list of clients
        self.send_message(f"Client at {addr} has disconnected\n")  # Send a message to all connected clients

    def display_clients(self):
        """
        This method displays the list of connected clients.
        """
        print("Connected clients:")
        for addr in self.clients:
            print(f'Client at {addr}\n')
    


if __name__ == "__main__":
    server = Server()
    server.start_server()
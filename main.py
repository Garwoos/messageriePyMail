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
        self.identifiers = {}  # New dictionary to store identifiers

    def start_server(self):
        """
        This method starts the server.
        """
        self.server.listen(15)  # the maximum queued connections
        print("Waiting for connection...\n")
        while True:
            client, addr = self.server.accept()
            print(f'A client has connected {addr}\n')
            if addr in self.clients:
                old_client = self.clients[addr]
                old_client.close()
            self.clients[addr] = client  # Add the client to the clients dictionary
            self.display_clients()  # Display the updated list of clients
            Thread(target=self.single_client, args=(client, addr)).start()  # Pass the address to single_client

    def generate_identifier(self, client, addr):
        """
        This function generates a unique identifier for a client.
        """
        identifier = None
        while not identifier or identifier in self.clients.keys():
            identifier = client.recv(1024).decode('utf-8') + '#'
            for i in range(4):
                identifier += f"{random.randint(0,9)}"
        self.clients[identifier] = client  # Store the client with the identifier as the key
        self.identifiers[addr] = identifier  # Add the address to the identifiers dictionary
        print(identifier + " has connected\n")
        return identifier


    def handle_client_messages(self, client, identifier):
        """
        This function handles the messages from a client.
        """
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f'Message from {identifier}: {message}')
                self.send_message_to_all_except_sender(identifier, message)
            except ConnectionResetError:
                print(f"Failed to receive message. Error: [WinError 10054] An existing connection was forcibly closed by the remote host")
                break

    def send_message_to_all_except_sender(self, sender_identifier, message):
        for identifier, client in self.clients.items():  # Now iterating over identifiers, not addresses
            if identifier != sender_identifier:  # Check the identifier directly
                client.send((f"{sender_identifier}: {message}").encode('utf-8'))  # Call send on the socket object
    
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
        """
        This method disconnects a client and updates the list of clients.
        """
        identifier = self.identifiers[addr]
        print(f'\nClient {identifier} has disconnected')  # Display the identifier of the disconnected client
        self.send_message(f"Client {identifier} has disconnected\n")  # Send a message to all connected clients
        del self.clients[identifier]  # Remove the client from the clients dictionary
        del self.identifiers[addr]  # Remove the address from the identifiers dictionary
        self.display_clients()  # Display the updated list of clients

    def display_clients(self):
        """
        This method displays the list of connected clients.
        """
        print("Connected clients:")
        for addr in self.clients:
            print(f'Client at {addr}\n')

    def send_message_prompt(self):
        choice = input("Do you want to send a message to a specific client or to all clients? (Enter 'specific' or 'all'): ")
        if choice.lower() == 'specific':
            self.send_message_to_specific_client()
        elif choice.lower() == 'all':
            message = input("Enter the message to send: ")
            self.send_message(message)
        else:
            print("Invalid choice. Please enter 'specific' or 'all'.")
        


if __name__ == "__main__":
    server = Server()
    server.start_server()
    while True:
        server.send_message_prompt()

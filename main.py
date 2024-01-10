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
        self.clients = {}

    def start_server(self):
        """
        This method starts the server.
        """
        self.server.listen(15)  # the maximum queued connections
        print("Waiting for connection...")
        while True:
            client, addr = self.server.accept()
            print(f'A client has connected {addr}')
            self.clients[addr] = client  # Add the client to the clients dictionary
            self.display_clients()  # Display the updated list of clients
            Thread(target=self.single_client, args=(client, addr)).start()  # Pass the address to single_client

    def single_client(self, client, addr):
        """
        This function handles a single client connection.
        """
        try:
            while True:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f'Message from client: {message}')
                
                response = "Message received by the server."
                client.send(response.encode('utf-8'))
        except ConnectionResetError:
            print("Client disconnected unexpectedly.")
        finally:
            self.disconnect_client(addr)  # Disconnect the client when it's done

    def send_message(self, message):
        """
        This method sends a message to all connected clients.
        """
        for addr in self.clients:
            self.clients[addr].send(message.encode('utf-8'))

    def disconnect_client(self, addr):
        """
        This method disconnects a client and updates the list of clients.
        """
        print(f'Client at {addr} has disconnected')  # Display the address of the disconnected client
        del self.clients[addr]  # Remove the client from the clients dictionary
        self.display_clients()  # Display the updated list of clients
        self.send_message(f"Client at {addr} has disconnected")  # Send a message to all connected clients

    def display_clients(self):
        """
        This method displays the list of connected clients.
        """
        print("Connected clients:")
        for addr in self.clients:
            print(f'Client at {addr}')

    def public_method(self):
        """
        This is a public method of the Server class.
        """
        pass  # Your code here

if __name__ == "__main__":
    server = Server()
    server.start_server()
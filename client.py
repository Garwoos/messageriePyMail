import socket

class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            identifier = input("Enter your identifier: ")  # Ask the user for an identifier
            self.send_message(identifier)  # Send the identifier to the server
            print(f'Connected to server {self.host}:{self.port}')
        except socket.error as e:
            print(f'Failed to connect to server {self.host}:{self.port}. Error: {e}')

    def send_message(self, message):
        self.client.sendall(message.encode('utf-8'))

    def receive_message(self):
        return self.client.recv(1024).decode('utf-8')

if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    while True :
        message = input("Enter message to send to server: ")
        client.send_message(message)
        print(client.receive_message())

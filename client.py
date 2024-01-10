import socket

class Client:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
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
    client.send_message("Hello, Server!")
    print(client.receive_message())
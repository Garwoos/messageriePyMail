import socket
import threading

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
        try:
            self.client.sendall(message.encode('utf-8'))
        except socket.error as e:
            print(f'Failed to send message. Error: {e}')

    def receive_message(self):
        try:
            return self.client.recv(1024).decode('utf-8')
        except socket.error as e:
            print(f'Failed to receive message. Error: {e}')

    def start_receiving_messages(self):
        thread = threading.Thread(target=self.receive_messages_in_loop, daemon=True)
        thread.start()

    def receive_messages_in_loop(self):
        while True:
            message = self.receive_message()
            if message:
                print(message)

if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    client.start_receiving_messages()  # Start the thread to receive messages
    while True:
        message = input("Enter a message to send: ")
        client.send_message(message)
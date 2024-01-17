import socket
import threading

class Client:
    def __init__(self, host='10.0.230.14', port=5555, identifier='Client1'):
        self.host = host
        self.port = port
        self.identifier = identifier
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            print(f'Connected to server {self.host}:{self.port}')
            self.send_message(self.identifier)  # Send the identifier to the server
            action = input("Do you want to (l)ogin or (r)egister? ")
            if action.lower() == 'l':
                self.login()
            elif action.lower() == 'r':
                self.register()
            else:
                print("Invalid choice. Please enter 'l' or 'r'.")
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
                if message == "Do you want to (l)ogin or (r)egister?":
                    action = input()
                    self.send_message(action)  # Send the user's choice to the server
                    if action.lower() == 'l':
                        self.login()
                    elif action.lower() == 'r':
                        self.register()
                    else:
                        print("Invalid choice. Please enter 'l' or 'r'.")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        self.send_message(f"LOGIN {username} {password}")

    def register(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        self.send_message(f"REGISTER {username} {password}")

if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    client.start_receiving_messages()  # Start the thread to receive messages
    while True:
        message = input()
        client.send_message(message)  # Send the user's message to the server
        if message.lower() == 'exit':
            break
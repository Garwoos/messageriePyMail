import socket
from threading import Thread
import time
import data_base

class Server:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.version = "1.0"
        self.clients = {}

    def start_server(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            return f'Server started on {self.host}:{self.port}'
        except socket.error as e:
            return f'Failed to start server on {self.host}:{self.port}. Error: {e}'

    def accept_connections(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected to {address[0]}:{address[1]}')
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        if self.check_version(client):
            client.send(b'True')
        else:
            client.send(b'False')
            client.close()
        while True:
            data = login(client).split(';')
            if data == ['True', 'admin']:
                client.send(b'True;admin')
                break
            elif data == ['True', 'user']:
                client.send(b'True;user')
                break
            else:
                client.send(b'False')

        while True:
            data = client.recv(1024).decode('utf-8')
            if data:
                print(data)
                send_message(client, 'Message received')

    def check_version(self, client):
        data = client.recv(1024).decode('utf-8')
        if data == self.version:
            return True
        else:
            return False


def login(client):
    data = client.recv(1024).decode('utf-8')
    print(data.split(';'))
    print([item for item in data_base.get_users()])
    if data.split(';') in [list(item[:2]) for item in data_base.get_users()]:
        if data_base.get_users()[[list(item[:2]) for item in data_base.get_users()].index(data.split(';'))][2] == 'True':
            print('Admin logged in')
            return f'True;admin'
        else:
            print('User logged in')
            return f'True;user'
    else:
        print('Failed to log in')
        return False


def send_message( client, message):
    client.send(message.encode('utf-8'))


if __name__ == '__main__':
    server = Server()
    print(server.start_server())
    server.accept_connections()

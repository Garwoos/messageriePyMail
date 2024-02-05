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
            if data[:2] == ['True', 'admin']:
                client.send(b'True;admin')
                break
            elif data[:2] == ['True', 'user']:
                client.send(b'True;user')
                break
            else:
                client.send(b'False')
        print(data)
        username = data[2]
        self.clients[username] = client
        print(f'Logged in as {username}')
        print(self.clients)
        data_base.add_user_group(f'{username}', 1)  # Ajouter l'utilisateur au groupe principal
        while True:
            data = client.recv(1024).decode('utf-8')
            if data:
                print(f"{username} : {data}")
                self.send_message_to_groupe(f'{username} : {data}', 1)

    def send_message_to_groupe(self, message, group_id):
        print(f'{data_base.get_users_from_group(group_id)}')
        for user_tuple in data_base.get_users_from_group(group_id):
            user = user_tuple[0]
            print(user)
            if user in self.clients:
                self.send_message(self.clients[user], message)
            else:
                print(f'User {user} not connected')

    def check_version(self, client):
        data = client.recv(1024).decode('utf-8')
        if data == self.version:
            return True
        else:
            return False

    def send_message(self,client, message):
        client.send(message.encode('utf-8'))


def login(client):
    data = client.recv(1024).decode('utf-8')
    print(data.split(';'))
    print([item for item in data_base.get_users()])
    if data.split(';') in [list(item[:2]) for item in data_base.get_users()]:
        if data_base.get_users()[[list(item[:2]) for item in data_base.get_users()].index(data.split(';'))][
                    2] == 'True':
            print('Admin logged in')
            return f'True;admin;{data.split(";")[0]}'
        else:
            print('User logged in')
            return f'True;user;{data.split(";")[0]}'
    else:
        print('Failed to log in')
        return False


if __name__ == '__main__':
    server = Server()
    print(server.start_server())
    server.accept_connections()

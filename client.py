import socket
import time
import threading


class Client:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.version = "1.0"

    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            print(f'Connected to server {self.host}:{self.port}')
            return True
        except socket.error as e:
            return f'Failed to connect to server {self.host}:{self.port}. Error: {e}'

    def send_version(self):
        try:
            self.client.sendto(f"{self.version}".encode('utf-8'), (self.host, self.port))
            return self.client.recv(1024)
        except socket.error as e:
            return f'Failed to send message. Error: {e}'

    def login(self, username, password):
        try:
            self.client.sendto(f"{username};{password}".encode('utf-8'), (self.host, self.port))
            return self.client.recv(1024).decode('utf-8')
        except socket.error as e:
            return f'Failed to send message. Error: {e}'

    def get_message_history(self, group_id):
        try:
            self.client.sendto(f"get_message_history;{group_id}".encode('utf-8'), (self.host, self.port))
            return self.client.recv(1024).decode('utf-8')
        except socket.error as e:
            return f'Failed to send message. Error: {e}'

    def send_message(self, message):
        try:
            self.client.sendto(f"{message}".encode('utf-8'), (self.host, self.port))
        except socket.error as e:
            return f'Failed to send message. Error: {e}'

    def get_message(self):
        try:
            return self.client.recv(1024).decode('utf-8')
        except socket.error as e:
            return f'Failed to receive message. Error: {e}'


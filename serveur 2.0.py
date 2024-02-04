from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
import threading
import json
import os
from datetime import datetime


class Server:
    """
    This class represents a server that can accept connections from clients.

    Attributes:
    host (str): The host on which the server is running.
    port (int): The port on which the server is listening.
    server (socket): The socket object representing the server.
    clients (dict): A dictionary to store connected clients.
    """

    def __init__(self):
        """
        The constructor for Server class. Initializes the server socket and starts listening for connections.
        """
        self.host = ""
        self.port = 5555
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(100)
        self.clients = {}
        self.version = "1.0"

    def __enter__(self):
        """
        Makes Server class compatible with 'with' statement. Returns the server instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures the server socket is closed when exiting a 'with' statement.
        """
        self.server.close()

    def start_server(self):
        """
        Starts the server and accepts connections from clients.
        """
        while True:
            # Accept a connection from the client
            client_socket, addr = self.server.accept()
            print(f'Connection established with {addr}')

            # Add the client to the server's clients dictionary
            self.clients[addr] = client_socket

            # Create a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, self))
            thread.start()

def check_version(self, version_user):
    """
    Function to check if the client version is compatible with the server version.

    Parameters:
    version (str): The version of the client.

    Returns:
    bool: True if the client version is compatible with the server version, False otherwise.
    """
    print(f"Server Version: {self.version}")
    print(f"Client Version: {version_user}")
    if self.version == version_user:
        return True
    else:
        return False


# Function to handle each client
def handle_client(client_socket, server):
    """
    Function to handle communication with a client. Receives messages from the client and processes them.

    Parameters:
    client_socket (socket): The socket object representing the client connection.
    server (Server): The instance of the Server class.
    """
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            # Use cut_message to extract client_socket, username, user_choice, message_content
            client_socket, username, user_choice, message_content = cut_message(message)

            # Call user_action with the extracted parameters
            user_action(client_socket, username, user_choice, message_content)


        except ConnectionResetError:
            print("Client disconnected.")
            break

    # Remove the client from the server's clients dictionary
    for addr, sock in server.clients.items():
        if sock == client_socket:
            del server.clients[addr]
            break

    client_socket.close()



# Function to store every ip address and port number of the clients connected to the server
def store_ipaddr_portnum_connected(addr):
    """
    Function to store the IP address and port number of each client connected to the server in a JSON file.

    Parameters:
    addr (tuple): The IP address and port number of the client.

    Returns:
    bool: True if the IP address and port number were stored successfully, False otherwise.
    """
    # Initialiser ipconnected en chargeant le fichier JSON s'il existe
    if os.path.exists('ipconnected/ipconnected.json'):
        try:
            with open('ipconnected/ipconnected.json', 'r') as ipconnected_file:
                ipconnected = json.load(ipconnected_file)
        except json.JSONDecodeError:
            print("Warning: The 'ipconnected.json' file is malformed. Resetting to an empty dictionary.")
            ipconnected = {}
    else:
        ipconnected = {}

    ip, port = addr  # Décomposer l'adresse en IP et port

    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Si l'IP existe déjà, ajouter les nouvelles informations à la liste existante
    # Sinon, créer une nouvelle liste pour cette IP
    if ip in ipconnected:
        ipconnected[ip].append({"port": port, "timestamp": timestamp})
    else:
        ipconnected[ip] = [{"port": port, "timestamp": timestamp}]

    try:
        with open('ipconnected/ipconnected.json', 'w') as ipconnected_file:
            json.dump(ipconnected, ipconnected_file, indent=4)
    except OSError as e:
        print(f"Error: Unable to write to the 'ipconnected/ipconnected.json' file. {str(e)}")
        return False

    return True


def search_data_in_group(group_name):
    """
    Function to search for data in a group. Returns the data if it exists.

    Parameters:
    group_name (str): The name of the group.

    Returns:
    dict: The data in the group if it exists, None otherwise.
    """
    try:
        with open('groups/groups.json', 'r') as groups_file:
            groups = json.load(groups_file)

    except json.JSONDecodeError:
        print("Error: The 'groups.json' file is malformed.")
        return None

    except OSError:
        print("Error: Unable to open the 'groups/groups.json' file.")
        return None

    if group_name not in groups:
        print(f"This group does not exist. Please try another group name.")
        return None

    return groups[group_name]


def search_message_group(group_name):
    """
    Function to search for messages in a group. Returns the messages if they exist.

    Parameters:
    group_name (str): The name of the group.

    Returns:
    dict: The messages in the group if they exist, None otherwise.
    """
    try:
        with open('groups/message_group.json', 'r') as message_group_file:
            message_group = json.load(message_group_file)

    except json.JSONDecodeError:
        print("Error: The 'message_group.json' file is malformed.")
        return None

    except OSError as e:
        print(f"Error: Unable to open the 'groups/message_group.json' file. {str(e)}")
        return None

    if group_name not in message_group:
        print(f"This group does not exist. Please try another group name.")
        return None

    return message_group[group_name]


def send_json_file(client_socket, group_name):
    """
    Function to send a JSON file to the client.

    Parameters:
    client_socket (socket): The socket object representing the client connection.
    file_path (str): The path to the JSON file.

    Returns:
    bool: True if the file was sent successfully, False otherwise.
    """
    # Get the data of the specific group
    data = search_data_in_group(group_name)

    # If the group data is None, then the group does not exist or an error occurred
    if data is None:
        print(f"Warning: Group '{group_name}' not found.")
        return

    # Convert the group data to a JSON string
    data_str = json.dumps(data)

    # get the message of the specific group
    message = search_message_group(group_name)

    # Check if either data_str or message is None before sending
    if data_str is not None:
        client_socket.sendall(data_str.encode())
    else:
        print("Error: 'data_str' is None.")

    if message is not None:
        messages_str = json.dumps(message)
        client_socket.sendall(messages_str.encode())
    else:
        print("Error: 'message' is None.")


def create_group(group_name):
    """
    Function to create a new group. Stores the group name in a JSON file.

    Parameters:
    group_name (str): The name of the new group.

    Returns:
    bool: True if the group was created successfully, False otherwise.
    """
    try:
        if not os.path.exists('groups/groups.json'):
            with open('groups/groups.json', 'w') as groups_file:
                json.dump({}, groups_file, indent=4)

        with open('groups/groups.json', 'r') as groups_file:
            groups = json.load(groups_file)

    except json.JSONDecodeError:
        print("Warning: The 'groups.json' file is malformed. Resetting to an empty dictionary.")
        groups = {}

    except OSError:
        print("Error: Unable to open the 'groups/groups.json' file.")
        return False

    if group_name in groups:
        print(f"This group already exists. Please try another group name.")
        return False

    groups[group_name] = {"members": []}

    try:
        with open('groups/groups.json', 'w') as groups_file:
            json.dump(groups, groups_file, indent=4)

    except OSError:
        print("Error: Unable to write to the 'groups.json' file.")
        return False

    return True


def add_member_to_group(group_name, username):
    """
    Function to add a member to a group. Stores the member name in a JSON file.

    Parameters:
    group_name (str): The name of the group.
    username (str): The name of the member.

    Returns:
    bool: True if the member was added successfully, False otherwise.
    """
    try:
        with open('groups/groups.json', 'r') as groups_file:
            groups = json.load(groups_file)

    except json.JSONDecodeError:
        print("Error: The 'groups/groups.json' file is malformed.")
        return False

    except OSError:
        print("Error: Unable to open the 'groups/groups.json' file.")
        return False

    if group_name not in groups:
        print(f"This group does not exist. Please try another group name.")
        return False

    if username in groups[group_name]["members"]:
        print(f"This member already exists. Please try another member name.")
        return False

    try:
        with open('users/users.json', 'r') as users_file:
            users = json.load(users_file)

    except json.JSONDecodeError:
        print("Error: The 'users.json' file is malformed.")
        return False

    if username not in users:
        print(f"This username does not exist. Please try another username.")
        return False

    groups[group_name]["members"].append(username)

    try:
        with open('groups/groups.json', 'w') as groups_file:
            json.dump(groups, groups_file, indent=4)

    except OSError:
        print("Error: Unable to write to the 'groups.json' file.")
        return False

    return True


def store_message_user(message, username):
    """
    Function to store the messages sent by each user in a JSON file.

    Parameters:
    message (str): The message sent by the user.
    username (str): The username of the user.

    Returns:
    bool: True if the message was stored successfully, False otherwise.
    """
    if os.path.exists('users/message_user.json'):
        try:
            with open('users/message_user.json', 'r') as file:
                message_user_dict = json.load(file)
        except json.JSONDecodeError:
            print("Warning: The 'users/message_user.json' file is malformed. Resetting to an empty dictionary.")
            message_user_dict = {}
    else:
        message_user_dict = {}

    current_time = datetime.now().strftime('%Y-%m-%d.%H:%M:%S')  # Get the current time with reduced precision

    if username in message_user_dict:
        message_user_dict[username].append({"message": message, "time": current_time})
    else:
        message_user_dict[username] = [{"message": message, "time": current_time}]

    try:
        with open('users/message_user.json', 'w') as file:
            json.dump(message_user_dict, file, indent=4)
    except Exception as e:
        print(f"Error: Unable to write to the 'message_user.json' file. Error details: {str(e)}")
        return False

    return True


def store_message_group(user, message, group_name):
    """
    Function to store the messages sent by each group in a JSON file.

    Parameters:
    message (str): The message sent by the group.
    group_name (str): The name of the group.

    Returns:
    bool: True if the message was stored successfully, False otherwise.
    """
    if os.path.exists('groups/message_group.json'):
        try:
            with open('groups/message_group.json', 'r') as file:
                message_group_dict = json.load(file)
        except json.JSONDecodeError:
            print("Warning: The 'groups/message_group.json' file is malformed. Resetting to an empty dictionary.")
            message_group_dict = {}
    else:
        message_group_dict = {}

    current_time = datetime.now().strftime('%Y-%m-%d.%H:%M:%S')  # Get the current time with reduced precision

    if group_name in message_group_dict:
        message_group_dict[group_name].append({"user": user, "message": message, "time": current_time})
    else:
        message_group_dict[group_name] = [{"user": user, "message": message, "time": current_time}]

    try:
        with open('groups/message_group.json', 'w') as file:
            json.dump(message_group_dict, file, indent=4)
    except Exception as e:
        print(f"Error: Unable to write to the 'message_group.json' file. Error details: {str(e)}")
        return False

    return True


# Function to create a new account
def register(username, password):
    """
    Function to create a new account. Stores the username and password in a JSON file.

    Parameters:
    username (str): The username for the new account.
    password (str): The password for the new account.

    Returns:
    bool: True if the account was created successfully, False otherwise.
    """
    try:
        if not os.path.exists('users/users.json'):
            with open('users/users.json', 'w') as users_file:
                json.dump({}, users_file, indent=4)

        with open('users/users.json', 'r') as users_file:
            users = json.load(users_file)

    except json.JSONDecodeError:
        print("Warning : The 'users/users.json' file is malformed. Resetting to an empty dictionary.")
        users = {}
    except OSError:
        print("Error: Unable to open the 'users/users.json' file.")
        return False

    if username in users:
        print(f"This username already exists. Please try username.")
        return False

    time = datetime.now().strftime('%Y-%m-%d.%H:%M:%S')  # Get the current time with reduced precision
    users[username] = {"password": password, "time": time}
    try:
        with open('users/users.json', 'w') as users_file:
            json.dump(users, users_file, indent=4)

    except OSError:
        print("Error: Unable to write to the 'users.json' file.")
        return False

    return True


def login(username, password):
    """
    Function to log in to an existing account. Checks if the username and password match.

    Parameters:
    username (str): The username for the account.
    password (str): The password for the account.

    Returns:
    bool: True if the login was successful, False otherwise.
    """
    try:
        with open('users/users.json', 'r') as users_file:
            users = json.load(users_file)

    except json.JSONDecodeError:
        print("Error: The 'users/users.json' file is malformed.")
        return False

    except OSError:
        print("Error: Unable to open the 'users/users.json' file.")
        return False

    if username not in users or users[username] != password:
        return False

    return True


# clientsocket&_&&--@\&username&_&&--@\user_choice&_&&--@\message
def cut_message(message):
    """
    Parameters:
    message (str): The message sent by the user.

    Returns:
    str: The username.
    str: The password.
    str: The group name.
    """
    client_socket = message.split("&_&&--@\\&")[0]
    username = message.split("&_&&--@\\&")[1]
    user_choice = message.split("&_&&--@\\&")[2]
    message = message.split("&_&&--@\\&")[3]

    return client_socket, username, user_choice, message


def user_action(client_socket, username, user_choice, message):
    """
    Function to choose between every data sent by the client.

    Parameters:
    message (str): The message sent by the user.

    Returns:
    bool: True if the choice was successful, False otherwise.
    """

    match user_choice:
        case "login":
            client_socket.sendall(login(username, message))

        case "register":
            client_socket.sendall(register(username, message))

        case "create_group":
            create_group(message)

        case "add_member_to_group":
            add_member_to_group(message, username)

        case "send_message":
            group_name, message_content = message.split("&_&&--@\&")
            store_message_user(message_content, username)
            store_message_group(username, message_content, group_name)

        case "get_new_message":
            group_name = message.split("&_&&--@\&")[0]
            send_json_file(client_socket, group_name)


def main():
    """
    The main function that starts the server and accepts connections from clients.
    """
    with Server() as server:
        while True:
            # Accept a connection from the client
            client_socket, addr = server.server.accept()
            print(f'Connection established with {addr}')

            # Add the client to the server's clients dictionary
            server.clients[addr] = client_socket

            # Create a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, server))
            thread.start()





if __name__ == "__main__":
    """
    The entry point for the script. Calls the main function.
    """
    main()

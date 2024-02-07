import tkinter as tk
from tkinter import messagebox
import time
import threading
import client
import notif

password = b'password'
client = client.Client()

connected = False

channels = ["main", "test"]


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.channel = tk.StringVar()

    def create_widgets(self):
        self.input = tk.Entry(self)
        self.input.grid(row=1, column=0, columnspan=3, sticky='ew')

        self.entry_button = tk.Button(self)
        self.entry_button["text"] = "Send"
        self.entry_button["command"] = self.send_message
        self.entry_button.grid(row=1, column=3, sticky='ew')

        self.message_box = tk.Text(self)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.grid(row=0, column=0, columnspan=4)

        self.channel_list = tk.Listbox(self)
        self.channel_list.grid(row=0, column=5, rowspan=2, sticky='ns')
        for channel in channels:
            self.channel_list.insert(tk.END, channel)

    def send_message(self):
        message = self.input.get()
        self.input.delete(0, tk.END)
        client.send_message(message)
        print('Message sent')

    def print_message(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, f"{message}\n")
        self.message_box.config(state=tk.DISABLED)
        print('Message printed')


class Connexion(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self)
        self.username_label["text"] = "Username"
        self.username_label.grid(row=0, column=0)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self)
        self.password_label["text"] = "Password"
        self.password_label.grid(row=1, column=0)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        self.connexion_button = tk.Button(self)
        self.connexion_button["text"] = "Connect"
        self.connexion_button["command"] = self.connect
        self.connexion_button.grid(row=2, column=0, columnspan=2)

    def connect(self):
        global connected
        global app
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            return
        message = client.login(username, password)
        print(message)

        if message.split(';') == ['True', 'admin']:
            print('logged in as admin')
            connected = True
            self.destroy()
            app = Application(master=root)
            thread = threading.Thread(target=get_message)
            thread.start()

        elif message.split(';') == ['True', 'user']:
            print('logged in as user')
            connected = True
            self.destroy()
            app = Application(master=root)
            thread = threading.Thread(target=get_message)
            thread.start()

        else:
            create_popup('Username or password incorrect')


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        client.client.close()


def create_popup(message):
    messagebox.showinfo('Error', message)


def get_message():
    while True:
        data = client.get_message()
        if data:
            app.print_message(f"{data}")
            if not is_window_focused(app):
                notif.send_notification('New message', f"{data}", 5)
            time.sleep(1)


def is_window_focused(self):
    focused_widget = self.master.focus_get()
    if focused_widget is None:
        return False
    else:
        return True


if __name__ == '__main__':
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    client.connect_to_server()
    if client.send_version() == 'True':
        print('Version sent')
    else:
        print('Failed to send version')
    if not connected:
        app = Connexion(master=root)
        app.mainloop()
    if connected:
        app = Application(master=root)
        app.mainloop()

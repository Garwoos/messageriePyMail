import tkinter as tk
import data_base

class DataBaseEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Base Editor")

        self.create_widgets()

    def create_widgets(self):
        InterfaceAddUser(self).grid(row=0, column=0, sticky="nsew")
        InterfaceAddGroup(self).grid(row=1, column=0, sticky="nsew")
        InterfaceAddUserGroup(self).grid(row=0, column=1, sticky="nsew")


class InterfaceAddUserGroup(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.frame_add_user_group = tk.Frame(self, relief="solid", borderwidth=2)
        self.frame_add_user_group.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.title_label_add_user_group = tk.Label(self.frame_add_user_group, text="Add user to group")
        self.title_label_add_user_group.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.label_add_user_group_username = tk.Label(self.frame_add_user_group, text="Username")
        self.label_add_user_group_username.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.label_add_user_group_idgroup = tk.Label(self.frame_add_user_group, text="Idgroup")
        self.label_add_user_group_idgroup.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.label_add_user_group_message = tk.Label(self.frame_add_user_group, text="Message")
        self.label_add_user_group_message.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.entry_add_user_group_username = tk.Entry(self.frame_add_user_group)
        self.entry_add_user_group_username.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.entry_add_user_group_idgroup = tk.Entry(self.frame_add_user_group)
        self.entry_add_user_group_idgroup.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.entry_add_user_group_message = tk.Entry(self.frame_add_user_group)
        self.entry_add_user_group_message.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.save_button_add_user_group = tk.Button(self.frame_add_user_group, text="Save", command=self.save)
        self.save_button_add_user_group.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def save(self):
        data_base.add_user_group(
            self.entry_add_user_group_username.get(),
            self.entry_add_user_group_idgroup.get(),
            self.entry_add_user_group_message.get()
        )
        self.entry_add_user_group_username.delete(0, "end")
        self.entry_add_user_group_idgroup.delete(0, "end")
        self.entry_add_user_group_message.delete(0, "end")

class InterfaceAddGroup(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.frame_add_group = tk.Frame(self, relief="solid", borderwidth=2)
        self.frame_add_group.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.title_label_add_group = tk.Label(self.frame_add_group, text="Add group")
        self.title_label_add_group.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.label_add_group_idgroup = tk.Label(self.frame_add_group, text="Idgroup")
        self.label_add_group_idgroup.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.label_add_group_group_name = tk.Label(self.frame_add_group, text="Group name")
        self.label_add_group_group_name.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.entry_add_group_idgroup = tk.Entry(self.frame_add_group)
        self.entry_add_group_idgroup.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.entry_add_group_group_name = tk.Entry(self.frame_add_group)
        self.entry_add_group_group_name.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.save_button_add_group = tk.Button(self.frame_add_group, text="Save", command=self.save)
        self.save_button_add_group.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def save(self):
        data_base.add_group(
            self.entry_add_group_idgroup.get(),
            self.entry_add_group_group_name.get()
        )
        self.entry_add_group_idgroup.delete(0, "end")
        self.entry_add_group_group_name.delete(0, "end")

class InterfaceAddUser(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.check_var = tk.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        self.frame_add_user = tk.Frame(self, relief="solid", borderwidth=2)
        self.frame_add_user.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.title_label_add_user = tk.Label(self.frame_add_user, text="Add user")
        self.title_label_add_user.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.label_add_user_username = tk.Label(self.frame_add_user, text="Username")
        self.label_add_user_username.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.label_add_user_password = tk.Label(self.frame_add_user, text="Password")
        self.label_add_user_password.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.entry_add_user_username = tk.Entry(self.frame_add_user)
        self.entry_add_user_username.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.entry_add_user_password = tk.Entry(self.frame_add_user)
        self.entry_add_user_password.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.check_button_add_user_admin = tk.Checkbutton(self.frame_add_user, text="Admin ?")
        self.check_button_add_user_admin.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        self.save_button_add_user = tk.Button(self.frame_add_user, text="Save", command=self.save)
        self.save_button_add_user.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    def save(self):
        data_base.add_user(
            self.entry_add_user_username.get(),
            self.entry_add_user_password.get(),
            f"self.check_var.get()"
        )
        self.entry_add_user_username.delete(0, "end")
        self.entry_add_user_password.delete(0, "end")
        self.check_var.set(False)


if __name__ == "__main__":
    app = DataBaseEditor()
    app.mainloop()
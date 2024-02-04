import customtkinter


class Connexion(customtkinter.CTk):
    """
    This class represents the login window of the application.
    It inherits from the customtkinter.CTk class.
    """

    def __init__(self, fg_color="gray30", text_color="#ffffff", border_color="gray50", border_width=5, corner_radius=6):
        """
        Initialize the Connexion window with username and password fields.
        """
        super().__init__()
        self.resizable(False, False)
        self.username_input = ""
        self.password_input = ""

        # Create username and password fields
        self.usernames = MyEntry(self, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                 border_color=border_color, border_width=border_width)
        self.usernames.grid(row=0, column=0, padx=10, pady=10)

        self.password = MyPasswordEntry(self, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                        border_color=border_color, border_width=border_width, show='*')
        self.password.grid(row=1, column=0, padx=10, pady=10)

        # Create a button for submitting the login form
        self.entry_button_frame = MyConnexionButton(self, "Connexion", self.usernames, self.password,
                                                    fg_color=fg_color, corner_radius=corner_radius,
                                                    text_color=text_color,
                                                    border_color=border_color, border_width=border_width)
        self.entry_button_frame.grid(row=2, column=0, padx=10, pady=10)

        # Create a label for displaying error messages
        self.error_message = MyLabel(self, text="Error : None", fg_color="#ff0000", corner_radius=corner_radius,
                                     text_color=text_color)
        self.error_message.grid(row=0, column=1, padx=10, pady=10)

    def get_user_input(self):
        """
        Get the username and password entered by the user.
        """
        username_input, password_input = self.username_input, self.password_input
        self.username_input, self.password_input = "", ""
        return username_input, password_input

    def set_error_message(self, message):
        """
        Set the error message to be displayed.
        """
        self.error_message.configure(text=f"Error : {message}")


class App(customtkinter.CTk):
    """
    This class represents the main window of the application.
    It inherits from the customtkinter.CTk class.
    """

    def __init__(self, fg_color="gray30", text_color="#ffffff", border_color="gray50", border_width=5, corner_radius=0):
        """
        Initialize the main window with a list of users and a text box for messages.
        """
        super().__init__()
        self.geometry("1600x900")
        self.minsize(400, 220)
        self.maxsize(1920, 1080)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.user = ["self"]

        self.last_user_input = ""

        # Create a frame for the list of users
        self.channel_frame = MyScrollableRadiobuttonFrame(self, "Message", values=self.user, fg_color=fg_color,
                                                              text_color=text_color, corner_radius=corner_radius)
        self.channel_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsw")

        self.user_frame = MyScrollableRadiobuttonFrame(self, "Utilisateurs", values=self.user, fg_color=fg_color,
                                                                text_color=text_color, corner_radius=corner_radius)
        self.user_frame.grid(row=0, column=7, rowspan=2, padx=10, pady=10, sticky="nsw")

        # Create a text box for messages
        self.textbox_frame = MyTextBox(self, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                       border_color=border_color, border_width=border_width)
        self.textbox_frame.grid(row=0, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Create an entry field for new messages
        self.entry_frame = MyEntry(self, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                   border_color=border_color, border_width=border_width)
        self.entry_frame.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Create a button for sending messages
        self.entry_button_frame = MyEntryButton(self, "Envoyer", self.entry_frame, self.textbox_frame,
                                                fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                                border_color=border_color, border_width=border_width)
        self.entry_button_frame.grid(row=1, column=5, padx=10, pady=10, sticky="nsew")

    def get_last_user_input(self):
        """
        Get the last message entered by the user.
        """
        return self.last_user_input


class MyScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    """
    A custom scrollable frame for radio buttons.

    Attributes:
        master: The parent widget.
        title: The title of the frame.
        values: The values for the radio buttons.
        fg_color: The foreground color of the frame.
        text_color: The text color of the frame.
        corner_radius: The corner radius of the frame.
    """

    def __init__(self, master, title, values, fg_color, text_color, corner_radius):
        super().__init__(master, corner_radius=corner_radius)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color=fg_color, corner_radius=corner_radius,
                                            text_color=text_color)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.update(values)
        self.radiobuttons[0].select()

    def update(self, values=str):
        """
        Update the radio buttons in the frame.

        Args:
            values (str): The new values for the radio buttons.
        """
        # Remove existing radio buttons
        for radiobutton in self.radiobuttons:
            radiobutton.destroy()
        self.radiobuttons = []

        # Update the list of users
        self.values = values

        # Create new radio buttons for each user
        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable,
                                                       fg_color="gray30", text_color="#ffffff",
                                                       border_color="gray50",
                                                       corner_radius=0)  # change corner radius
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="nsew")
            self.radiobuttons.append(radiobutton)

    def get(self):
        """
        Get the current value of the radio buttons.

        Returns:
            The current value of the radio buttons.
        """
        return self.variable.get()

    def set(self, value):
        """
        Set the current value of the radio buttons.

        Args:
            value: The new value for the radio buttons.
        """
        self.variable.set(value)


class MyTextBox(customtkinter.CTkTextbox):
    """
    A custom text box class that inherits from customtkinter.CTkTextbox.

    Attributes:
        master: The parent widget.
        text_color: The color of the text.
        fg_color: The foreground color.
        corner_radius: The radius of the corners.
        border_color: The color of the border.
        border_width: The width of the border.
    """

    def __init__(self, master, text_color, fg_color, corner_radius, border_color, border_width):
        """
        Initialize the text box.

        Args:
            master: The parent widget.
            text_color: The color of the text.
            fg_color: The foreground color.
            corner_radius: The radius of the corners.
            border_color: The color of the border.
            border_width: The width of the border.
        """
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width)
        # Disable the textbox so the user cannot edit it.
        self.configure(state='disabled')

    def print(self, text):
        """
        Print text to the text box.

        Args:
            text (str): The text to be printed to the text box.
        """
        self.configure(state='normal')
        self.insert('end', text + "\n")
        self.configure(state='disabled')

    def clear(self):
        """
        Clear the text box.
        """
        self.configure(state='normal')
        self.delete('1.0', 'end')
        self.configure(state='disabled')

    def get_text(self):
        """
        Get the text from the text box.

        Returns:
            str: The text in the text box.
        """
        return self.get('1.0', 'end')


class MyEntry(customtkinter.CTkEntry):
    """
    A custom entry field that inherits from customtkinter.CTkEntry.

    Attributes:
        master: The parent widget.
        text_color: The color of the text.
        fg_color: The foreground color.
        corner_radius: The radius of the corners.
        border_color: The color of the border.
        border_width: The width of the border.
    """

    def __init__(self, master, text_color, fg_color, corner_radius, border_color, border_width):
        """
        Initialize the entry field.

        Args:
            master: The parent widget.
            text_color: The color of the text.
            fg_color: The foreground color.
            corner_radius: The radius of the corners.
            border_color: The color of the border.
            border_width: The width of the border.
        """
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width)
        self.var = customtkinter.StringVar()
        self['textvariable'] = self.var
        self.bind('<KeyRelease>', self._update_var)

    def _update_var(self, event):
        """
        Update the variable with the current text in the entry field.

        Args:
            event: The event information.
        """
        self.var.set(self.get())

    def get_text(self):
        """
        Get the text from the entry field.

        Returns:
            str: The text in the entry field.
        """
        print(f"Getting text: {self.var.get()}")
        return self.var.get()


class MyPasswordEntry(customtkinter.CTkEntry):
    """
    A custom password entry field that inherits from customtkinter.CTkEntry.

    Attributes:
        master: The parent widget.
        text_color: The color of the text.
        fg_color: The foreground color.
        corner_radius: The radius of the corners.
        border_color: The color of the border.
        border_width: The width of the border.
        show: The character used to mask the password. If None, the password is shown as is.
    """

    def __init__(self, master, text_color, fg_color, corner_radius, border_color, border_width, show=None):
        """
        Initialize the password entry field.

        Args:
            master: The parent widget.
            text_color: The color of the text.
            fg_color: The foreground color.
            corner_radius: The radius of the corners.
            border_color: The color of the border.
            border_width: The width of the border.
            show: The character used to mask the password. If None, the password is shown as is.
        """
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width)
        self.show = show
        self.var = customtkinter.StringVar()
        self['textvariable'] = self.var
        if self.show is not None:
            self.configure(show=self.show)
            self.bind('<KeyRelease>', self._update_var)

    def _update_var(self, event):
        """
        Update the variable with the current text in the entry field.

        Args:
            event: The event information.
        """
        self.var.set(self.get())

    def get_text(self):
        """
        Get the text from the entry field.

        Returns:
            str: The text in the entry field.
        """
        print(f"Getting text: {self.var.get()}")
        return self.var.get()


class MyEntryButton(customtkinter.CTkButton):
    """
    A custom button class that inherits from customtkinter.CTkButton.

    Attributes:
        master: The parent widget.
        text: The text displayed on the button.
        entry_frame: The entry field associated with the button.
        textbox_frame: The text box associated with the button.
        fg_color: The foreground color of the button.
        corner_radius: The radius of the corners of the button.
        text_color: The color of the text on the button.
        border_color: The color of the border of the button.
        border_width: The width of the border of the button.
    """

    def __init__(self, master, text, entry_frame, textbox_frame, fg_color, corner_radius, text_color, border_color,
                 border_width):
        """
        Initialize the button.

        Args:
            master: The parent widget.
            text: The text displayed on the button.
            entry_frame: The entry field associated with the button.
            textbox_frame: The text box associated with the button.
            fg_color: The foreground color of the button.
            corner_radius: The radius of the corners of the button.
            text_color: The color of the text on the button.
            border_color: The color of the border of the button.
            border_width: The width of the border of the button.
        """
        self.entry_frame = entry_frame
        self.textbox_frame = textbox_frame
        super().__init__(master, text=text, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width, command=self.get_text_and_print)

    def get_text_and_print(self):
        """
        Get the text from the entry field and print it to the text box.

        If the text is empty, the function returns without doing anything.
        Otherwise, the text is deleted from the entry field and printed to the text box.
        """
        text = self.entry_frame.get_text()
        if text == "":
            return
        self.master.last_user_input = text
        self.entry_frame.delete(0, 'end')  # Delete the text from the entry
        self.textbox_frame.print(text)  # Print the text to the textbox


class MyConnexionButton(customtkinter.CTkButton):
    """
    A custom button class for the login form that inherits from customtkinter.CTkButton.

    Attributes:
        master: The parent widget.
        text: The text displayed on the button.
        usernames: The username entry field associated with the button.
        password: The password entry field associated with the button.
        fg_color: The foreground color of the button.
        corner_radius: The radius of the corners of the button.
        text_color: The color of the text on the button.
        border_color: The color of the border of the button.
        border_width: The width of the border of the button.
    """

    def __init__(self, master, text, usernames, password, fg_color, corner_radius, text_color, border_color,
                 border_width):
        """
        Initialize the button.

        Args:
            master: The parent widget.
            text: The text displayed on the button.
            usernames: The username entry field associated with the button.
            password: The password entry field associated with the button.
            fg_color: The foreground color of the button.
            corner_radius: The radius of the corners of the button.
            text_color: The color of the text on the button.
            border_color: The color of the border of the button.
            border_width: The width of the border of the button.
        """
        self.usernames = usernames
        self.password = password
        super().__init__(master, text=text, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width, command=self.verify_correctness)

    def verify_correctness(self):
        """
        Verify the correctness of the username and password.

        The function gets the username and password from the associated entry fields.
        If the username is empty, the function returns without doing anything.
        Otherwise, the username and password are stored in the master's username_input and password_input attributes,
        and the text in the entry fields is deleted.
        """
        username = self.usernames.get_text()
        print(f"Username: {username}")
        password = self.password.get_text()
        print(f"Password: {password}")
        if username == "":
            return
        self.master.username_input = username
        self.usernames.delete(0, 'end')
        self.master.password_input = password
        self.password.delete(0, 'end')


class MyLabel(customtkinter.CTkLabel):
    """
    A custom label class that inherits from customtkinter.CTkLabel.

    Attributes:
        master: The parent widget.
        text: The text displayed on the label.
        fg_color: The foreground color of the label.
        corner_radius: The radius of the corners of the label.
        text_color: The color of the text on the label.
    """

    def __init__(self, master, text, fg_color, corner_radius, text_color):
        """
        Initialize the label.

        Args:
            master: The parent widget.
            text: The text displayed on the label.
            fg_color: The foreground color of the label.
            corner_radius: The radius of the corners of the label.
            text_color: The color of the text on the label.
        """
        super().__init__(master, text=text, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color)

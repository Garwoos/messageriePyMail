import customtkinter


class App(customtkinter.CTk):
    def __init__(self, fg_color="gray30", text_color="gray40", border_color="gray50", border_width=5, corner_radius=6):
        super().__init__()
        self.geometry("1600x900")
        self.minsize(400, 220)
        self.maxsize(1920, 1080)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.user = []

        self.last_user_input = ""

        self.radiobutton_frame = MyScrollableRadiobuttonFrame(self, "Message", values=self.user, fg_color=fg_color,
                                                              text_color=text_color, corner_radius=corner_radius)
        self.radiobutton_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.textbox_frame = MyTextBox(self, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                       border_color=border_color, border_width=border_width)
        self.textbox_frame.grid(row=0, column=1, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.entry_frame = MyEntry(self, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                   border_color=border_color, border_width=border_width)
        self.entry_frame.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.entry_button_frame = MyEntryButton(self, "Envoyer", self.entry_frame, self.textbox_frame,
                                                fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                                                border_color=border_color, border_width=border_width)
        self.entry_button_frame.grid(row=1, column=5, padx=10, pady=10, sticky="nsew")

    def get_last_user_input(self):
        return self.last_user_input


class MyScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values, fg_color, text_color, corner_radius):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color=fg_color, corner_radius=corner_radius,
                                            text_color=text_color)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.update(values)

    def update(self, values=str):
        # Supprimer les boutons radio existants
        for radiobutton in self.radiobuttons:
            radiobutton.destroy()
        self.radiobuttons = []

        # Mettre à jour la liste des utilisateurs
        self.values = values

        # Créer de nouveaux boutons radio pour chaque utilisateur
        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="nsew")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)


class MyTextBox(customtkinter.CTkTextbox):
    def __init__(self, master, text_color, fg_color, corner_radius, border_color, border_width):
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width)
        # Disable the textbox so the user cannot edit it.
        self.configure(state='disabled')

    def print(self, text):
        """
        This method is used to print text to the textbox.

        Parameters:
        text (str): The text to be printed to the textbox.
        """
        self.configure(state='normal')
        self.insert('end', text + "\n")
        self.configure(state='disabled')


class MyEntry(customtkinter.CTkEntry):
    def __init__(self, master, text_color, fg_color, corner_radius, border_color, border_width):
        super().__init__(master, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width)

    def get_text(self):
        return self.get()


class MyEntryButton(customtkinter.CTkButton):
    def __init__(self, master, text, entry_frame, textbox_frame, fg_color, corner_radius, text_color, border_color,
                 border_width):
        self.entry_frame = entry_frame
        self.textbox_frame = textbox_frame
        super().__init__(master, text=text, fg_color=fg_color, corner_radius=corner_radius, text_color=text_color,
                         border_color=border_color, border_width=border_width, command=self.get_text_and_print)

    def get_text_and_print(self):
        text = self.entry_frame.get_text()
        if text == "":
            return
        self.master.last_user_input = text
        self.entry_frame.delete(0, 'end')  # Delete the text from the entry
        self.textbox_frame.print(text)  # Print the text to the textbox

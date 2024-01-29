import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1600x900")
        self.minsize(400, 220)
        self.maxsize(1920, 1080)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.user = []

        self.radiobutton_frame = MyScrollableRadiobuttonFrame(self, "Message", values=self.user)
        self.radiobutton_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        self.textbox_frame = MyTextBox(self)
        self.textbox_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

class MyScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.update(values)

    def update(self, values):
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
    def __init__(self, master):
        super().__init__(master, fg_color="gray30", corner_radius=6, text_color="red", bg_color="gray90", border_color="gray30", border_width=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
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

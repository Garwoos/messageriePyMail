import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("1600x900")
        self.minsize(400, 220)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)

        user = [f"User {i}" for i in range(1, 11)]

        self.radiobutton_frame = MyScrollableRadiobuttonFrame(self, "Message", values=user)
        self.radiobutton_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="nsw")

        self.textbox_frame = MyScrollableTextBox(self)
        self.textbox_frame.grid(row=0, column=6, padx=(10),columnspan=5, pady=(10), sticky="nsew")

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

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="nsew")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class MyScrollableTextBox(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.textbox = customtkinter.CTkTextbox(self, fg_color="gray30", corner_radius=6)
        self.textbox.grid(row=0, column=0, padx=10, pady=(10), sticky="nsew")


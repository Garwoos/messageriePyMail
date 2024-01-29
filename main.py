import interface_graphique

user = []

if __name__ == '__main__':
    app = interface_graphique.App()
    app.title("Discord mais en moin bien")
    app.radiobutton_frame.update(user)
    app.textbox_frame.print("Hello world!")
    app.mainloop()

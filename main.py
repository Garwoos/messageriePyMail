import interface_graphique
if __name__ == '__main__':
    app = interface_graphique.App()
    app.title("My app")
    app.textbox_frame.print("Hello world!")
    app.mainloop()

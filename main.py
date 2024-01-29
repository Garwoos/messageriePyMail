import interface_graphique

user = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]

if __name__ == '__main__':
    app = interface_graphique.App()
    app.title("Discord mais en moin bien")
    app.radiobutton_frame.update(user)
    app.textbox_frame.print("Hello world! \n" * 100)
    app.mainloop()

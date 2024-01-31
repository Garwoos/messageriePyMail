import interface_graphique

users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]
identify = False
identifiant = ("mael", "1234")


def update_users():
    global users
    app.radiobutton_frame.update(users)
    app.after(1000, update_users)


def user_connexion():
    username, password = app.get_user_input()
    if (username, password) == identifiant:
        global identify
        identify = True
        app.destroy()
        return
    app.after(1000, user_connexion)


if __name__ == '__main__':
    if not identify:
        app = interface_graphique.Connexion()
        user_connexion()
        app.mainloop()
    if identify:
        app = interface_graphique.App()
        app.mainloop()

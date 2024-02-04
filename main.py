import interface_graphique

users = ["self", "user1"]
identify = True
identifiant = ("a", "a")
chanel = {}


def charger_chanel():
    global chanel
    chanel = {"self": "self", "user1": "user1"}


def get_user_chanel():
    print(app.radiobutton_frame.get())


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
        update_users()
        app.mainloop()

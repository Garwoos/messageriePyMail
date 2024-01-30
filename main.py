import interface_graphique

users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]


def update_users():
    global users
    app.radiobutton_frame.update(users)
    app.after(1000, update_users)

def user_connexion():
    global users
    username, password = app.get_user_input()
    app.after(1000, user_connexion)

if __name__ == '__main__':
    app = interface_graphique.connexion()
    app.title("Connexion")


    app.mainloop()

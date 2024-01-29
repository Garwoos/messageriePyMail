import interface_graphique

users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]


def update_users():
    global users
    app.radiobutton_frame.update(users)
    app.after(1000, update_users)


if __name__ == '__main__':
    app = interface_graphique.App(fg_color=None, text_color=None, border_color=None, border_width=5,
                                  corner_radius=6)
    app.title("Discord mais en moin bien")
    update_users()
    app.textbox_frame.print("Hello world! \n" * 100)

    app.mainloop()

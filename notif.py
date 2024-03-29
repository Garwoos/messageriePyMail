from plyer import notification
import winsound
import chime

def sound_notification():
    """
    Joue un son de notification.
    """
    winsound.Beep(440, 1)
    chime.theme('mario')
    chime.error()

def send_notification(title, message, timeout):
    """
    Envoie une notification.

    Parameters:
        title (str): Le titre de la notification.
        message (str): Le contenu de la notification.
        timeout (int): La durée en secondes pour afficher la notification.
    """
    notification.notify(
        title=title,
        message=message,
        timeout=timeout,
        app_name='PyCommChat',
        app_icon='icon.ico',
        ticker='Nouveau message !',
        toast=False
    )
    sound_notification()


if __name__ == '__main__':
    send_notification('Nouveau message !', 'Vous avez reçu un nouveau message.', 5)
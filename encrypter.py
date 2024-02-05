from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def generer_cle(secret, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(secret)


def encrypter_message(message, cle):
    iv = os.urandom(16)  # vecteur d'initialisation
    cipher = Cipher(algorithms.AES(cle), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    message_chiffre = encryptor.update(message) + encryptor.finalize()
    return iv + message_chiffre


def decrypter_message(message_chiffre, cle):
    iv = message_chiffre[:16]
    message_chiffre = message_chiffre[16:]
    cipher = Cipher(algorithms.AES(cle), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    message_decrypte = decryptor.update(message_chiffre) + decryptor.finalize()
    return message_decrypte

if __name__ == '__main__':
    mot_de_passe = b"mot_de_passe_secret"
    sel = os.urandom(16)  # sel (salt) aléatoire

    cle = generer_cle(mot_de_passe, sel)

    message_original = b"Ceci est un message secret."

    message_chiffre = encrypter_message(message_original, cle)
    print("Message chiffré:", message_chiffre)

    message_decrypte = decrypter_message(message_chiffre, cle)
    print("Message déchiffré:", message_decrypte.decode('utf-8'))
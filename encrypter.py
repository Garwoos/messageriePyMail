from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Crypt:

    def __init__(self):
        self.private_key_pem = self.charger_cle_privee()
        self.public_key_pem = self.charger_cle_publique()

    def charger_cle_privee(self):
        with open('secrets_keys/private_key.pem', 'rb') as f:
            private_key_pem = f.read()
        return private_key_pem

    def charger_cle_publique(self):
        with open('secrets_keys/public_key.pem', 'rb') as f:
            public_key_pem = f.read()
        return public_key_pem

    def encrypt(self, message):
        public_key = serialization.load_pem_public_key(self.public_key_pem, backend=default_backend())
        cipher_text = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipher_text

    def decrypt(self, cipher_text):
        private_key = serialization.load_pem_private_key(self.private_key_pem, password=None, backend=default_backend())
        decrypted_message = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()
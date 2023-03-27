import os
import base64
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from basic_gui import *


# GUI with encryption/decryption capabilities
class CipheredGUI(BasicGUI):
    def __init__(self) -> None:
        super().__init__()
        self.key = None

    # Override the _create_connection_window() method to add a password field
    def _create_connection_window(self):
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name","pswd"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(
                        default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            dpg.add_button(label="Connect", callback=self.run_chat)

    # Override the run_chat() method to retrieve the password and derive the key
    def run_chat(self, sender, app_data):
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("pswd")

        self._log.info(f"Connecting {name}@{host}:{port}")
        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

        self.key = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=16,
            salt=b"JuStSoMeSaLt",
            iterations=100000,
            backend=default_backend()
        ).derive(bytes(password, "utf-8"))

    # Encrypt a message and return a tuple of bytes (iv, encrypted)
    def encrypt(self, message):
        iv = os.urandom(16)
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.CTR(iv),
            backend=default_backend()
        ).encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(bytes(message, "utf-8")) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv, encrypted

    # Decrypt a message and return a UTF-8 string
    def decrypt(self, message):
        iv = base64.b64decode(message[0]['data'])
        message = base64.b64decode(message[1]['data'])
        decryptor = Cipher(
            algorithms.AES(self.key),
            modes.CTR(iv),
            backend=default_backend()
        ).decryptor()
        decrypted_data = decryptor.update(message) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data.decode("utf-8")

    def send(self, text):
        # Encrypt the message
        message = self.encrypt(text)
        self._client.send_message(message)

    def recv(self) -> None:
        if self._callback is not None:
            for user, message in self._callback.get():
                message = self.decrypt(message)
                self.update_text_screen(f"{user} : {message}")
            self._callback.clear()


if __name__ == "__main__":
    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()
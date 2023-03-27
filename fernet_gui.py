from ciphered_gui import CipheredGUI
import hashlib
import base64
import logging

from cryptography.fernet import Fernet


class FernetGUI(CipheredGUI):
    """A class that extends CipheredGUI to create FernetGUI,
    which uses authenticated symmetric encryption"""

    def run_chat(self, sender, app_data) -> None:
     
        # Get connection info
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_pswd")
        self._log.info(f"Connecting {name}@{host}:{port}")

        # Set up callback, start client, and register name
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # Hide connection window and show chat window
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

        # Generate encryption key using password
        password_bytes = bytes(password, 'utf-8')
        key = base64.urlsafe_b64encode(hashlib.sha256(password_bytes).digest())

    def encrypt(self, message) -> bytes:
        """Redefined function that encrypts the given message"""
        # Convert message to bytes
        message_bytes = bytes(message, 'utf-8') 
        # Encrypt message using Fernet
        fernet = Fernet(self.key)
        encrypted_message = fernet.encrypt(message_bytes)
        return encrypted_message

    def decrypt(self, message) -> str:
        """Redefined function that decrypts the given message"""
        message_bytes = base64.urlsafe_b64decode(message['data'])
        fernet = Fernet(self.key)
        decrypted_message = fernet.decrypt(message_bytes).decode('utf-8')
        return decrypted_message


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # Instantiate the FernetGUI class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()
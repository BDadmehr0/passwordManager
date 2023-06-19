from sys import exit, argv
from PyQt6.QtWidgets import QApplication
from UserInterface.passwordManager import PasswordManager


if __name__ == "__main__":
    # TODO: make login window
    app = QApplication(argv)
    app.setStyle("Fusion")
    window = PasswordManager()
    exit(app.exec())

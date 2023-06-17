from sys import exit, argv
from PyQt6.QtWidgets import QApplication
from UserInterface.passwordManager import PasswordManager

if __name__ == "__main__":
    app = QApplication(argv)
    window = PasswordManager()
    exit(app.exec())
from sys import exit, argv
from PyQt6.QtWidgets import QApplication
from UserInterface.passwordManager import PasswordManager


if __name__ == "__main__":
    appVersion = "V00.1E.C4"
    app = QApplication(argv)
    app.setStyle("Fusion")
    window = PasswordManager(appVersion)
    exit(app.exec())

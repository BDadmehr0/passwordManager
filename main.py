from sys import exit, argv
from mainApp import MainApp


if __name__ == "__main__":
    app = MainApp(argv)
    exit(app.exec())

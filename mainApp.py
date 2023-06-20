import json
from os import makedirs
from os.path import exists
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from UserInterface.passwordManager import PasswordManager
import darkdetect
from sheetStyle.darkTheme import darkTheme
from sheetStyle.lightTheme import lightTheme
from qt_material import apply_stylesheet
from screeninfo import get_monitors

class MainApp():
    def __init__(self, argv) -> None:
        self.dataFilesPath = ".\\Data\\"
        self.dataFileName = ".\\data.json"
        self.data = self.loadData()
        self.settingsFileName = self.data["settingsFileName"]
        self.loadSettings()
        self.app = QApplication(argv)
        self.setAppStyleAndTheme()
        screenSize = self.findScreenSize()
        self.mainWindow = PasswordManager(self.data["appVersion"], self, screenSize[0], screenSize[1], self.dataFilesPath, self.data["secretsFileName"], self.data["settingsFileName"], self.data["mainPasswordFileName"])

    def findScreenSize(self) -> tuple:
        for monitor in get_monitors():
            if monitor.is_primary:
                screenWidth = monitor.width
                screenHeight = monitor.height
        return (screenWidth, screenHeight)

    def setAppStyleAndTheme(self) -> None:
        self.app.setStyle(self.appStyle)
        if self.theme == "Dark":
            self.app.setStyleSheet(darkTheme)
        elif self.theme == "Light":
            self.app.setStyleSheet(lightTheme)
        elif self.theme == "System":
            pass
        else:
            theme = self.selectTheme(self.theme)
            apply_stylesheet(self.app, theme, self.appStyle)

    def selectTheme(self, theme) -> str:
        if theme == "Dark amber":
            theme = "dark_amber.xml"
        elif theme == "Dark blue":
            theme = "dark_blue.xml"
        elif theme == "Dark cyan":
            theme = "dark_cyan.xml"
        elif theme == "Dark lightgreen":
            theme = "dark_lightgreen.xml"
        elif theme == "Dark pink":
            theme = "dark_pink.xml"
        elif theme == "Dark purple":
            theme = "dark_purple.xml"
        elif theme == "Dark red":
            theme = "dark_red.xml"
        elif theme == "Dark teal":
            theme = "dark_teal.xml"
        elif theme == "Dark yellow":
            theme = "dark_yellow.xml"
        elif theme == "Light amber":
            theme = "light_amber.xml"
        elif theme == "Light blue":
            theme = "light_blue.xml"
        elif theme == "Light cyan":
            theme = "light_cyan.xml"
        elif theme == "Light cyan 500":
            theme = "light_cyan_500.xml"
        elif theme == "Light lightgreen":
            theme = "light_lightgreen.xml"
        elif theme == "Light pink":
            theme = "light_pink.xml"
        elif theme == "Light purple":
            theme = "light_purple.xml"
        elif theme == "Light red":
            theme = "light_red.xml"
        elif theme == "Light teal":
            theme = "light_teal.xml"
        elif theme == "Light yellow":
            theme = "light_yellow.xml"
        return theme

    def loadData(self) -> dict:
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.dataFileName)):
                file = open(
                    Path(self.dataFilesPath, self.dataFileName), "r", encoding="utf-8"
                )
                data = json.load(file)
                file.close()
                return data
            else:
                file = open(Path(self.dataFilesPath, self.dataFileName), "x")
                data = {}
                json.dump(data, file)
                file.close()
                self.loadData()
        else:
            makedirs(Path(self.dataFilesPath))
            self.loadData()

    def loadSettings(self) -> None:
        file = open(
            Path(self.dataFilesPath, self.settingsFileName), "r", encoding="utf-8"
        )
        data = json.load(file)
        file.close()
        for row in data:
            if row == "theme":
                if data[row] == "Auto":
                    if darkdetect.isDark():
                        self.theme = "Dark"
                    else:
                        self.theme = "Light"
                else:
                    self.theme = data[row]
            elif row == "appStyle":
                self.appStyle = data[row]

    def saveData(self) -> None:
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.dataFileName)):
                file = open(Path(self.dataFilesPath, self.dataFileName), "w")
                json.dump(self.data, file)
                file.close()
            else:
                file = open(Path(self.dataFilesPath, self.dataFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilesPath))
            self.saveData()

    def exec(self) -> int:
        self.saveData()
        return self.app.exec()

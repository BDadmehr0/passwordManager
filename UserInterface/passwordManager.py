import json
from os import makedirs
from os.path import exists
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtCore import QSize, QTimer, Qt, QPointF
from UserInterface.appRow import AppRow
from UserInterface.addNewItem import AddNewItem
from UserInterface.setting import SettingWindow
from UserInterface.login import Login
from UserInterface.okAlert import OKAlert


class PasswordManager(QWidget):
    def __init__(self, appVersion: str, mainApp, screenWidth: int, screenHeight: int, dataFilesPath: str, secretsFileName: str, settingsFileName: str, mainPasswordFileName: str, parent=None) -> None:
        super().__init__(parent)
        self.mainApp = mainApp
        self.appVersion = appVersion
        self.dataFilesPath = dataFilesPath
        self.secretsFileName = secretsFileName
        self.settingsFileName = settingsFileName
        self.mainPasswordFileName = mainPasswordFileName
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.windowWidth = 1000
        self.windowHeight = 800
        self.clockCounterVariable = 0
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.oldPosition = QPointF(self.screenWidth, self.screenHeight)
        self.setupUi()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockCount)
        self.clock.start(10)
        self.isLoginValid = False
        self.loginAttempts = 0
        self.loginWindow()

    def setupUi(self) -> None:
        self.setWindowTitle("Password Manager")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setGeometry((self.screenWidth - self.windowWidth) // 2, (self.screenHeight - self.windowHeight) // 2, self.windowWidth, self.windowHeight)
        self.setWindowIcon(QIcon("Assets\\password.png"))
        self.passwordManagerLayout = QVBoxLayout()
        self.header = QHBoxLayout()
        self.appNameAndIconLayout = QHBoxLayout()
        self.appIconLabel = QLabel("")
        self.appIconLabel.setPixmap(QIcon("Assets\\password.png").pixmap(QSize(16, 16)))
        self.appNameAndIconLayout.addWidget(self.appIconLabel)
        self.appNamaLabel = QLabel("Password Manager")
        self.appNameAndIconLayout.addWidget(self.appNamaLabel)
        self.appNameAndIconLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.header.addLayout(self.appNameAndIconLayout)
        self.dragAndDropAreaLayout = QHBoxLayout()
        self.dragAndDropAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.header.addLayout(self.dragAndDropAreaLayout)
        self.appButtonsLayout = QHBoxLayout()
        self.minimizePushButton = QPushButton(QIcon("Assets\\minimize.png"), "")
        self.minimizePushButton.clicked.connect(self.showMinimized)
        self.appButtonsLayout.addWidget(self.minimizePushButton)
        self.maximizeOrRestoreDownPushButton = QPushButton(QIcon("Assets\\expand.png"), "")
        self.maximizeOrRestoreDownPushButton.clicked.connect(self.maximizeOrRestore)
        self.appButtonsLayout.addWidget(self.maximizeOrRestoreDownPushButton)
        self.closePushButton = QPushButton(QIcon("Assets\\close.png"), "")
        self.closePushButton.clicked.connect(self.closeWindow)
        self.appButtonsLayout.addWidget(self.closePushButton)
        self.appButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.header.addLayout(self.appButtonsLayout)
        self.passwordManagerLayout.addLayout(self.header)
        self.mainAppLayout = QVBoxLayout()
        self.settingPushButton = QPushButton(QIcon("Assets\\setting.png"), "Setting")
        self.settingPushButton.clicked.connect(self.settingWindow)
        self.mainAppLayout.addWidget(self.settingPushButton)
        self.appHeader = QHBoxLayout()
        self.nameHeaderLabel = QLabel("Name")
        self.appHeader.addWidget(self.nameHeaderLabel)
        self.usernameHeaderLabel = QLabel("Username")
        self.appHeader.addWidget(self.usernameHeaderLabel)
        self.passwordHeaderLabel = QLabel("Password")
        self.appHeader.addWidget(self.passwordHeaderLabel)
        self.addNewItemPushButton = QPushButton(QIcon("Assets\\add_new.png"), "Add new item")
        self.addNewItemPushButton.clicked.connect(self.addNewItemWindow)
        self.addNewItemPushButton.setMaximumWidth(140)
        self.appHeader.addWidget(self.addNewItemPushButton)
        self.mainAppLayout.addLayout(self.appHeader)
        self.appScrollArea = QScrollArea()
        self.scrollAreaLayoutContents = QVBoxLayout()
        self.scrollAreaLayoutContents.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.appScrollArea.setLayout(self.scrollAreaLayoutContents)
        self.mainAppLayout.addWidget(self.appScrollArea)
        self.passwordManagerLayout.addLayout(self.mainAppLayout)
        self.footer = QHBoxLayout()
        self.statusLayout = QHBoxLayout()
        self.timeLabel = QLabel("00:00:00:00")
        self.statusLayout.addWidget(self.timeLabel)
        self.appStatusLabel = QLabel("Ready.")
        self.statusLayout.addWidget(self.appStatusLabel)
        self.statusLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.footer.addLayout(self.statusLayout)
        self.versionLayout = QHBoxLayout()
        self.versionLabel = QLabel(self.appVersion)
        self.versionLayout.addWidget(self.versionLabel)
        self.versionLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.footer.addLayout(self.versionLayout)
        self.auteurLayout = QHBoxLayout()
        self.auteurIconLabel = QLabel("")
        self.auteurIconLabel.setPixmap(QIcon("Assets\\AriAas.png").pixmap(QSize(16, 16)))
        self.auteurLayout.addWidget(self.auteurIconLabel)
        self.auteurNameLabel = QLabel("AriAas")
        self.auteurLayout.addWidget(self.auteurNameLabel)
        self.auteurLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.footer.addLayout(self.auteurLayout)
        self.passwordManagerLayout.addLayout(self.footer)
        self.setLayout(self.passwordManagerLayout)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.oldPosition = a0.globalPosition()
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self.oldPosition.y() - self.y() < 40:
            delta = QPointF(a0.globalPosition() - self.oldPosition)
            self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
            self.oldPosition = a0.globalPosition()
        return super().mouseMoveEvent(a0)

    def clockCount(self) -> None:
        self.clockCounterVariable += 1
        milliseconds = self.clockCounterVariable
        seconds, milliseconds = divmod(milliseconds, 100)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.timeLabel.setText("{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, milliseconds))

    def maximizeOrRestore(self) -> None:
        if self.isMaximized():
            self.showNormal()
            self.maximizeOrRestoreDownPushButton.setIcon(QIcon("Assets\\expand.png"))
        else:
            self.showMaximized()
            self.maximizeOrRestoreDownPushButton.setIcon(QIcon("Assets\\collapse.png"))

    def addNewItemWindow(self) -> None:
        self.addNewItemWindowUi = AddNewItem(self.appVersion, self.screenWidth, self.screenHeight)
        self.addNewItemWindowUi.submitClicked.connect(self.addNewItemWindowConfirm)

    def addNewItemWindowConfirm(self, name, username, password):
        self.scrollAreaLayoutContents.addLayout(AppRow(name, username, password, self.screenWidth,self.screenHeight, self.appVersion))

    def settingWindow(self) -> None:
        self.close()
        self.settingWindowUi = SettingWindow(self.appVersion, self.screenWidth, self.screenHeight, self.dataFilesPath, self.secretsFileName, self.settingsFileName, self.mainPasswordFileName)
        self.settingWindowUi.submitClicked.connect(self.settingWindowConfirm)

    def settingWindowConfirm(self, isOkPressed):
        if isOkPressed:
            self.close()
            self.mainApp.setAppStyleAndTheme()
            self.__init__(self.appVersion, self.mainApp, self.screenWidth, self.screenHeight, self.dataFilesPath, self.secretsFileName, self.settingsFileName, self.mainPasswordFileName)
        else:
            self.show()

    def alertWindow(self, message) -> None:
        self.alertWindow = OKAlert(message, self.appVersion, self.screenWidth, self.screenHeight)

    def loginWindow(self) -> None:
        self.settingWindowUi = Login(self.appVersion, self.screenWidth, self.screenHeight, self.dataFilesPath, self.mainPasswordFileName)
        self.settingWindowUi.submitClicked.connect(self.loginWindowConfirm)

    def loginWindowConfirm(self, isLoginValid):
        if isLoginValid:
            self.isLoginValid = True
            self.show()
            self.loadData()
        else:
            self.loginAttempts += 1
            if self.loginAttempts == 3:
                self.alertWindow("You did enter the wrong password three times!")
                self.close()
            else:
                self.loginWindow()

    def saveData(self) -> None:
        # TODO: encrypt data
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.secretsFileName)):
                file = open(Path(self.dataFilesPath, self.secretsFileName), "w")
                data = {}
                rowNumber = 1
                for row in self.scrollAreaLayoutContents.children():
                    data[f"row-{rowNumber}"] = {}
                    data[f"row-{rowNumber}"]["name"] = row.nameLineEdit.text()
                    data[f"row-{rowNumber}"]["username"] = row.usernameLineEdit.text()
                    data[f"row-{rowNumber}"]["password"] = row.passwordLineEdit.text()
                    rowNumber += 1
                json.dump(data, file)
                file.close()
            else:
                file = open(Path(self.dataFilesPath, self.secretsFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilesPath))
            self.saveData()

    def loadData(self) -> None:
        # TODO: decrypt data
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.secretsFileName)):
                file = open(Path(self.dataFilesPath, self.secretsFileName), "r", encoding="utf-8")
                data = json.load(file)
                file.close()
                for row in data:
                    self.scrollAreaLayoutContents.addLayout(AppRow(data[row]["name"], data[row]["username"], data[row]["password"], self.screenWidth, self.screenHeight, self.appVersion))
            else:
                file = open(Path(self.dataFilesPath, self.secretsFileName), "x")
                data = {}
                json.dump(data, file)
                file.close()
        else:
            makedirs(Path(self.dataFilesPath))
            self.loadData()

    def closeWindow(self) -> None:
        if self.isLoginValid:
            self.saveData()
        self.close()

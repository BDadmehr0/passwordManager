import json
from os import makedirs
from os.path import exists
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QStyleFactory
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtCore import QSize, QTimer, Qt, QPointF, pyqtSignal
from UserInterface.passwordCheck import PasswordCheck
from UserInterface.changePassword import ChangePassword


class SettingWindow(QWidget):
    submitClicked = pyqtSignal(bool)

    def __init__(self, appVersion: str, screenWidth: int, screenHeight: int, dataFilesPath: str, secretsFileName: str, settingsFileName: str, mainPasswordFileName: str, parent=None) -> None:
        super().__init__(parent)
        self.appVersion = appVersion
        self.dataFilesPath = dataFilesPath
        self.secretsFileName = secretsFileName
        self.settingsFileName = settingsFileName
        self.mainPasswordFileName = mainPasswordFileName
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.windowWidth = 1000
        self.windowHeight = 800
        self.passwordCheckAttempts = 0
        self.clockCounterVariable = 0
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.oldPosition = QPointF(self.screenWidth, self.screenHeight)
        self.setupUi()
        self.loadSetting()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockCount)
        self.clock.start(10)
        self.show()

    def setupUi(self) -> None:
        self.setWindowTitle("Setting")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setGeometry((self.screenWidth - self.windowWidth) // 2, (self.screenHeight - self.windowHeight) // 2, self.windowWidth, self.windowHeight)
        self.setWindowIcon(QIcon("Assets\\password.png"))
        self.settingWindowLayout = QVBoxLayout()
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
        self.settingWindowLayout.addLayout(self.header)
        self.mainSettingWindowLayout = QVBoxLayout()
        self.themeLayout = QHBoxLayout()
        self.themeLabel = QLabel("Theme:")
        self.themeLayout.addWidget(self.themeLabel)
        self.themeComboBox = QComboBox()
        self.themeComboBox.addItem("Auto")
        self.themeComboBox.addItem("System")
        self.themeComboBox.addItem("Dark")
        self.themeComboBox.addItem("Light")
        self.themeComboBox.addItem("Dark amber")
        self.themeComboBox.addItem("Dark blue")
        self.themeComboBox.addItem("Dark cyan")
        self.themeComboBox.addItem("Dark light green")
        self.themeComboBox.addItem("Dark pink")
        self.themeComboBox.addItem("Dark purple")
        self.themeComboBox.addItem("Dark red")
        self.themeComboBox.addItem("Dark teal")
        self.themeComboBox.addItem("Dark yellow")
        self.themeComboBox.addItem("Light amber")
        self.themeComboBox.addItem("Light blue")
        self.themeComboBox.addItem("Light cyan")
        self.themeComboBox.addItem("Light cyan 500")
        self.themeComboBox.addItem("Light light green")
        self.themeComboBox.addItem("Light pink")
        self.themeComboBox.addItem("Light purple")
        self.themeComboBox.addItem("Light red")
        self.themeComboBox.addItem("Light teal")
        self.themeComboBox.addItem("Light yellow")
        self.themeLayout.addWidget(self.themeComboBox)
        self.mainSettingWindowLayout.addLayout(self.themeLayout)
        self.appStyleLayout = QHBoxLayout()
        self.appStyleLabel = QLabel("App style:")
        self.appStyleLayout.addWidget(self.appStyleLabel)
        self.appStyleComboBox = QComboBox()
        for style in QStyleFactory.keys():
            if style == "Fusion":
                self.appStyleComboBox.addItem("Fusion")
            elif style == "Windows":
                self.appStyleComboBox.addItem("Windows")
            elif style == "windowsvista":
                self.appStyleComboBox.addItem("Windows vista")
            elif style == "WindowsXP":
                self.appStyleComboBox.addItem("Windows XP")
            elif style == "QtCurve":
                self.appStyleComboBox.addItem("QtCurve")
            elif style == "Oxygen":
                self.appStyleComboBox.addItem("Oxygen")
            elif style == "Breeze":
                self.appStyleComboBox.addItem("Breeze")
            elif style == "Android":
                self.appStyleComboBox.addItem("Android")
            elif style == "Macintosh":
                self.appStyleComboBox.addItem("Macintosh")
        self.appStyleLayout.addWidget(self.appStyleComboBox)
        self.mainSettingWindowLayout.addLayout(self.appStyleLayout)
        self.changePasswordLayout = QHBoxLayout()
        self.changePasswordButton = QPushButton("Change main password")
        self.changePasswordButton.clicked.connect(self.changePassword)
        self.changePasswordLayout.addWidget(self.changePasswordButton)
        self.mainSettingWindowLayout.addLayout(self.changePasswordLayout)
        self.resetFactoryLayout = QHBoxLayout()
        self.resetFactoryButton = QPushButton("Reset factory")
        self.resetFactoryButton.clicked.connect(self.resetFactory)
        self.resetFactoryLayout.addWidget(self.resetFactoryButton)
        self.mainSettingWindowLayout.addLayout(self.resetFactoryLayout)
        self.submitButtonsLayout = QHBoxLayout()
        self.submitButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.ok)
        self.submitButtonsLayout.addWidget(self.okButton)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel)
        self.submitButtonsLayout.addWidget(self.cancelButton)
        self.mainSettingWindowLayout.addLayout(self.submitButtonsLayout)
        self.settingWindowLayout.addLayout(self.mainSettingWindowLayout)
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
        self.settingWindowLayout.addLayout(self.footer)
        self.setLayout(self.settingWindowLayout)

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

    def closeWindow(self) -> None:
        self.close()

    def cancel(self) -> None:
        self.submitClicked.emit(False)
        self.closeWindow()

    def ok(self) -> None:
        self.saveData()
        self.submitClicked.emit(True)
        self.closeWindow()

    def changePassword(self) -> None:
        self.changePasswordWindow = ChangePassword(self.appVersion, self.screenWidth, self.screenHeight, self.dataFilesPath, self.mainPasswordFileName)
        self.changePasswordWindow.submitClicked.connect(self.changePasswordWindowConfirm)

    def changePasswordWindowConfirm(self, returnCode, newPassword) -> None:
        if returnCode == 0:
            self.saveNewPassword(newPassword)
        elif returnCode == 2:
            self.closeWindow()

    def resetFactory(self) -> None:
        self.passwordCheckWindow()

    def passwordCheckWindow(self) -> None:
        self.settingWindowUi = PasswordCheck(self.appVersion, self.screenWidth, self.screenHeight, self.dataFilesPath, self.mainPasswordFileName)
        self.settingWindowUi.submitClicked.connect(self.passwordCheckWindowConfirm)

    def passwordCheckWindowConfirm(self, isPasswordCorrect) -> None:
        if isPasswordCorrect:
            self.clearData()
        else:
            self.passwordCheckAttempts += 1
            if self.passwordCheckAttempts == 3:
                self.closeWindow()
            else:
                self.passwordCheckWindow()

    def clearData(self) -> None:
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.secretsFileName)):
                file = open(Path(self.dataFilesPath, self.secretsFileName), "w")
                data = {}
                json.dump(data, file)
                file.close()
            else:
                file = open(Path(self.dataFilesPath, self.secretsFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilesPath))
            self.saveData()

    def saveNewPassword(self, newPassword) -> None:
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.mainPasswordFileName)):
                file = open(Path(self.dataFilesPath, self.mainPasswordFileName), "w")
                data = {"mainPassword": newPassword}
                json.dump(data, file)
                file.close()
            else:
                file = open(Path(self.dataFilesPath, self.mainPasswordFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilesPath))
            self.saveData()

    def saveData(self) -> None:
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.settingsFileName)):
                file = open(Path(self.dataFilesPath, self.settingsFileName), "w")
                data = {}
                for row in self.mainSettingWindowLayout.children():
                    for index in range(row.count()):
                        if type(row.itemAt(index).widget()) == type(QLabel()):
                            if row.itemAt(index).widget().text() == "Theme:":
                                data["theme"] = (row.itemAt(index + 1).widget().currentText())
                            elif row.itemAt(index).widget().text() == "App style:":
                                data["appStyle"] = (row.itemAt(index + 1).widget().currentText())
                json.dump(data, file)
                file.close()
            else:
                file = open(Path(self.dataFilesPath, self.settingsFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilesPath))
            self.saveData()

    def loadSetting(self) -> None:
        if exists(Path(self.dataFilesPath)):
            if Path.is_file(Path(self.dataFilesPath, self.settingsFileName)):
                file = open(Path(self.dataFilesPath, self.settingsFileName), "r", encoding="utf-8")
                data = json.load(file)
                file.close()
                for row in data:
                    if row == "theme":
                        if data[row] == "Auto":
                            self.themeComboBox.setCurrentIndex(0)
                        elif data[row] == "System":
                            self.themeComboBox.setCurrentIndex(1)
                        elif data[row] == "Dark":
                            self.themeComboBox.setCurrentIndex(2)
                        elif data[row] == "Light":
                            self.themeComboBox.setCurrentIndex(3)
                        elif data[row] == "Dark amber":
                            self.themeComboBox.setCurrentIndex(4)
                        elif data[row] == "Dark blue":
                            self.themeComboBox.setCurrentIndex(5)
                        elif data[row] == "Dark cyan":
                            self.themeComboBox.setCurrentIndex(6)
                        elif data[row] == "Dark light green":
                            self.themeComboBox.setCurrentIndex(7)
                        elif data[row] == "Dark pink":
                            self.themeComboBox.setCurrentIndex(8)
                        elif data[row] == "Dark purple":
                            self.themeComboBox.setCurrentIndex(9)
                        elif data[row] == "Dark red":
                            self.themeComboBox.setCurrentIndex(10)
                        elif data[row] == "Dark teal":
                            self.themeComboBox.setCurrentIndex(11)
                        elif data[row] == "Dark yellow":
                            self.themeComboBox.setCurrentIndex(12)
                        elif data[row] == "Light amber":
                            self.themeComboBox.setCurrentIndex(13)
                        elif data[row] == "Light blue":
                            self.themeComboBox.setCurrentIndex(14)
                        elif data[row] == "Light cyan":
                            self.themeComboBox.setCurrentIndex(15)
                        elif data[row] == "Light cyan 500":
                            self.themeComboBox.setCurrentIndex(16)
                        elif data[row] == "Light light green":
                            self.themeComboBox.setCurrentIndex(17)
                        elif data[row] == "Light pink":
                            self.themeComboBox.setCurrentIndex(18)
                        elif data[row] == "Light purple":
                            self.themeComboBox.setCurrentIndex(19)
                        elif data[row] == "Light red":
                            self.themeComboBox.setCurrentIndex(20)
                        elif data[row] == "Light teal":
                            self.themeComboBox.setCurrentIndex(21)
                        elif data[row] == "Light yellow":
                            self.themeComboBox.setCurrentIndex(22)
                    elif row == "appStyle":
                        if data[row] == "Fusion":
                            self.appStyleComboBox.setCurrentIndex(0)
                        elif data[row] == "Windows":
                            self.appStyleComboBox.setCurrentIndex(1)
                        elif data[row] == "Windows vista":
                            self.appStyleComboBox.setCurrentIndex(2)
                        elif data[row] == "Windows XP":
                            self.appStyleComboBox.setCurrentIndex(3)
                        elif data[row] == "QtCurve":
                            self.appStyleComboBox.setCurrentIndex(4)
                        elif data[row] == "Oxygen":
                            self.appStyleComboBox.setCurrentIndex(5)
                        elif data[row] == "Breeze":
                            self.appStyleComboBox.setCurrentIndex(6)
                        elif data[row] == "Android":
                            self.appStyleComboBox.setCurrentIndex(7)
                        elif data[row] == "Macintosh":
                            self.appStyleComboBox.setCurrentIndex(8)
            else:
                file = open(Path(self.dataFilesPath, self.settingsFileName), "x")
                data = {}
                json.dump(data, file)
                file.close()
        else:
            makedirs(Path(self.dataFilesPath))
            self.loadSetting()

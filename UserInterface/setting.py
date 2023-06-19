import json
from os import makedirs
from os.path import exists
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QScrollBar,
)
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtCore import QSize, QTimer, Qt, QPointF, pyqtSignal
from sheetStyle.darkMode import darkMode
from UserInterface.passwordCheck import PasswordCheck
import darkdetect


class SettingWindow(QWidget):
    submitClicked = pyqtSignal(bool)

    def __init__(self, appVersion: str = "V00.00.00", parent=None) -> None:
        super().__init__(parent)
        self.appVersion = appVersion
        self.dataFilePath = ".\\Data\\"
        self.dataFileName = ".\\data.json"
        self.settingFileName = ".\\setting.json"
        self.screenWidth = 1920
        self.screenHeight = 1080
        self.windowWidth = 1000
        self.windowHeight = 800
        self.passwordCheckAttempts = 0
        self.clockCounterVariable = 0
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.loadSetting()
        self.setupUi()
        self.loadData()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockCount)
        self.clock.start(10)
        self.show()

    def setupUi(self) -> None:
        if self.darkModeEnable == "Dark":
            self.setStyleSheet(darkMode)
        self.setWindowTitle("Setting")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(
            (self.screenWidth - self.windowWidth) // 2,
            (self.screenHeight - self.windowHeight) // 2,
            self.windowWidth,
            self.windowHeight,
        )
        self.setWindowIcon(QIcon("Assets\\password.png"))
        self.settingWindowLayout = QVBoxLayout()
        self.header = QHBoxLayout()
        self.appNameAndIconLayout = QHBoxLayout()
        self.appIconLabel = QLabel("")
        self.appIconLabel.setPixmap(
            QIcon("Assets\\password.png").pixmap(QSize(16, 16)))
        self.appNameAndIconLayout.addWidget(self.appIconLabel)
        self.appNamaLabel = QLabel("Password Manager")
        self.appNameAndIconLayout.addWidget(self.appNamaLabel)
        self.appNameAndIconLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.header.addLayout(self.appNameAndIconLayout)
        self.dragAndDropAreaLayout = QHBoxLayout()
        self.dragAndDropAreaLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.header.addLayout(self.dragAndDropAreaLayout)
        self.appButtonsLayout = QHBoxLayout()
        self.minimizePushButton = QPushButton(
            QIcon("Assets\\minimize.png"), "")
        self.minimizePushButton.clicked.connect(self.showMinimized)
        self.appButtonsLayout.addWidget(self.minimizePushButton)
        self.maximizeOrRestoreDownPushButton = QPushButton(
            QIcon("Assets\\expand.png"), ""
        )
        self.maximizeOrRestoreDownPushButton.clicked.connect(
            self.maximizeOrRestore)
        self.appButtonsLayout.addWidget(self.maximizeOrRestoreDownPushButton)
        self.closePushButton = QPushButton(QIcon("Assets\\close.png"), "")
        self.closePushButton.clicked.connect(self.closeWindow)
        self.appButtonsLayout.addWidget(self.closePushButton)
        self.appButtonsLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.header.addLayout(self.appButtonsLayout)
        self.settingWindowLayout.addLayout(self.header)
        self.mainSettingWindowLayout = QVBoxLayout()
        self.themeLayout = QHBoxLayout()
        self.themeLabel = QLabel("Theme:")
        self.themeLayout.addWidget(self.themeLabel)
        self.themeComboBox = QComboBox()
        self.themeComboBox.addItem("Auto")
        self.themeComboBox.addItem("Light")
        self.themeComboBox.addItem("Dark")
        self.themeLayout.addWidget(self.themeComboBox)
        self.mainSettingWindowLayout.addLayout(self.themeLayout)
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
        self.statusLayout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )
        self.footer.addLayout(self.statusLayout)
        self.versionLayout = QHBoxLayout()
        self.versionLabel = QLabel(self.appVersion)
        self.versionLayout.addWidget(self.versionLabel)
        self.versionLayout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        )
        self.footer.addLayout(self.versionLayout)
        self.auteurLayout = QHBoxLayout()
        self.auteurIconLabel = QLabel("")
        self.auteurIconLabel.setPixmap(
            QIcon("Assets\\AriAas.png").pixmap(QSize(16, 16))
        )
        self.auteurLayout.addWidget(self.auteurIconLabel)
        self.auteurNameLabel = QLabel("AriAas")
        self.auteurLayout.addWidget(self.auteurNameLabel)
        self.auteurLayout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )
        self.footer.addLayout(self.auteurLayout)
        self.settingWindowLayout.addLayout(self.footer)
        self.setLayout(self.settingWindowLayout)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.oldPosition = a0.globalPosition()
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self.oldPosition.y() - self.y() < 30:
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
        self.timeLabel.setText(
            "{:02d}:{:02d}:{:02d}:{:02d}".format(
                hours, minutes, seconds, milliseconds)
        )

    def maximizeOrRestore(self) -> None:
        if self.isMaximized():
            self.showNormal()
            self.maximizeOrRestoreDownPushButton.setIcon(
                QIcon("Assets\\expand.png"))
        else:
            self.showMaximized()
            self.maximizeOrRestoreDownPushButton.setIcon(
                QIcon("Assets\\collapse.png"))

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
        pass

    def resetFactory(self) -> None:
        self.passwordCheckWindow()

    def passwordCheckWindow(self) -> None:
        self.settingWindowUi = PasswordCheck(self.appVersion)
        self.settingWindowUi.submitClicked.connect(self.PasswordCheckWindowConfirm)

    def PasswordCheckWindowConfirm(self, isPasswordCorrect) -> None:
        if isPasswordCorrect:
            self.clearData()
        else:
            self.passwordCheckAttempts += 1
            if self.passwordCheckAttempts == 3:
                self.closeWindow()
            else:
                self.passwordCheckWindow()

    def clearData(self) -> None:
        if exists(Path(self.dataFilePath)):
            if Path.is_file(Path(self.dataFilePath, self.dataFileName)):
                file = open(Path(self.dataFilePath, self.dataFileName), "w")
                data = {}
                json.dump(data, file)
            else:
                file = open(Path(self.dataFilePath, self.dataFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilePath))
            self.saveData()

    def saveData(self) -> None:
        if exists(Path(self.dataFilePath)):
            if Path.is_file(Path(self.dataFilePath, self.settingFileName)):
                file = open(Path(self.dataFilePath, self.settingFileName), "w")
                data = {}
                for row in self.mainSettingWindowLayout.children():
                    for index in range(row.count()):
                        if type(row.itemAt(index).widget()) == type(QLabel()):
                            if row.itemAt(index).widget().text() == "Theme:":
                                data["theme"] = (
                                    row.itemAt(
                                        index + 1).widget().currentText()
                                )
                json.dump(data, file)
            else:
                file = open(Path(self.dataFilePath, self.settingFileName), "x")
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilePath))
            self.saveData()

    def loadData(self) -> None:
        if exists(Path(self.dataFilePath)):
            if Path.is_file(Path(self.dataFilePath, self.settingFileName)):
                file = open(
                    Path(self.dataFilePath, self.settingFileName), "r", encoding="utf-8"
                )
                data = json.load(file)
                file.close()
                for row in data:
                    if row == "theme":
                        if data[row] == "Auto":
                            self.themeComboBox.setCurrentIndex(0)
                        elif data[row] == "Light":
                            self.themeComboBox.setCurrentIndex(1)
                        elif data[row] == "Dark":
                            self.themeComboBox.setCurrentIndex(1)
                        else:
                            pass
            else:
                file = open(Path(self.dataFilePath, self.settingFileName), "x")
                data = {}
                json.dump(data, file)
                file.close()
        else:
            makedirs(Path(self.dataFilePath))
            self.loadData()

    def loadSetting(self) -> None:
        file = open(
            Path(self.dataFilePath, self.settingFileName), "r", encoding="utf-8"
        )
        data = json.load(file)
        file.close()
        for row in data:
            if row == "theme":
                if data[row] == "Auto":
                    if darkdetect.isDark():
                        self.darkModeEnable = "Dark"
                    else:
                        self.darkModeEnable = "Light"
                elif data[row] == "Light":
                    self.darkModeEnable = "Light"
                elif data[row] == "Dark":
                    self.darkModeEnable = "Dark"
                else:
                    pass

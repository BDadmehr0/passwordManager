import json
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QPointF
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)
from UserInterface.passwordGenerator import PasswordGenerator
from sheetStyle.darkMode import darkMode
import darkdetect


class PasswordCheck(QWidget):
    submitClicked = pyqtSignal(bool)

    def __init__(self, appVersion: str = "V00.00.00", parent=None) -> None:
        super().__init__(parent)
        self.appVersion = appVersion
        self.dataFilePath = ".\\Data\\"
        self.settingFileName = ".\\setting.json"
        self.mainPasswordFileName = ".\\mainPassword.json"
        self.screenWidth = 1920
        self.screenHeight = 1080
        self.windowWidth = 400
        self.windowHeight = 200
        self.clockCounterVariable = 0
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.loadSetting()
        self.setupUi()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockCount)
        self.clock.start(10)
        self.show()

    def setupUi(self) -> None:
        if self.darkModeEnable == "Dark":
            self.setStyleSheet(darkMode)
        self.setWindowTitle("Add new item")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(
            (self.screenWidth - self.windowWidth) // 2,
            (self.screenHeight - self.windowHeight) // 2,
            self.windowWidth,
            self.windowHeight,
        )
        self.setWindowIcon(QIcon("Assets\\password.png"))
        self.loginWindowLayout = QVBoxLayout()
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
        self.loginWindowLayout.addLayout(self.header)
        self.mainLoginWindowLayout = QVBoxLayout()
        self.passwordLayout = QHBoxLayout()
        self.passwordLabel = QLabel("Password:")
        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLineEdit = QLineEdit()
        self.passwordLayout.addWidget(self.passwordLineEdit)
        self.mainLoginWindowLayout.addLayout(self.passwordLayout)
        self.loginButtonLayout = QHBoxLayout()
        self.loginButton = QPushButton("Done")
        self.loginButton.clicked.connect(self.login)
        self.loginButtonLayout.addWidget(self.loginButton)
        self.mainLoginWindowLayout.addLayout(self.loginButtonLayout)
        self.loginWindowLayout.addLayout(self.mainLoginWindowLayout)
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
        self.loginWindowLayout.addLayout(self.footer)
        self.setLayout(self.loginWindowLayout)

    def closeWindow(self) -> None:
        self.close()

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

    def login(self) -> None:
        file = open(
            Path(self.dataFilePath, self.mainPasswordFileName), "r", encoding="utf-8"
        )
        data = json.load(file)
        file.close()
        for row in data:
            if row == "mainPassword":
                if self.passwordLineEdit.text() == data[row]:
                    self.submitClicked.emit(True)
                    self.closeWindow()
                else:
                    self.submitClicked.emit(False)
                    self.closeWindow()

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

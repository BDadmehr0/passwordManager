import json
from os import makedirs
from os.path import exists
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QScrollBar
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtCore import QSize, QTimer, Qt, QPointF, pyqtSignal
from UserInterface.appRow import AppRow
from UserInterface.addNewItem import AddNewItem


class SettingWindow(QWidget):
    submitClicked = pyqtSignal(bool)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.dataFilePath = ".\\Data\\"
        self.dataFileName = ".\\setting.json"
        self.screenWidth = 1920
        self.screenHeight = 1080
        self.windowWidth = 1000
        self.windowHeight = 800
        self.clockCounterVariable = 0
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.setupUi()
        self.loadData()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockCount)
        self.clock.start(10)
        self.show()

    def setupUi(self) -> None:
        self.setWindowTitle("Setting")
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
        
        self.footer = QHBoxLayout()
        self.statusLayout = QHBoxLayout()
        self.timeLabel = QLabel("00:00:00:00")
        self.statusLayout.addWidget(self.timeLabel)
        self.appStatusLabel = QLabel("Ready.")
        self.statusLayout.addWidget(self.appStatusLabel)
        self.statusLayout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.footer.addLayout(self.statusLayout)
        self.versionLayout = QHBoxLayout()
        self.versionLabel = QLabel("V00.01.19")
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

    def saveData(self) -> None:
        # TODO: encrypt data
        if exists(Path(self.dataFilePath)):
            if Path.is_file(Path(self.dataFilePath, self.dataFileName)):
                file = open(Path(self.dataFilePath, self.dataFileName), "w")
                data = {}
                for row in self.scrollAreaLayoutContents.children():
                    if row.rowNumber == 0:
                        self.numberOfPassword += 1
                        row.rowNumber = self.numberOfPassword
                    data[f"row-{row.rowNumber}"] = {}
                    data[f"row-{row.rowNumber}"]["rowNumber"] = str(row.rowNumber)
                    data[f"row-{row.rowNumber}"]["name"] = row.nameLineEdit.text()
                    data[f"row-{row.rowNumber}"]["username"] = row.usernameLineEdit.text()
                    data[f"row-{row.rowNumber}"]["password"] = row.passwordLineEdit.text()
                json.dump(data, file)
            else:
                file = open(Path(self.dataFilePath, self.dataFileName), 'x')
                file.close()
                self.saveData()
        else:
            makedirs(Path(self.dataFilePath))
            self.saveData()

    def loadData(self) -> None:
        # TODO: decrypt data
        if exists(Path(self.dataFilePath)):
            if Path.is_file(Path(self.dataFilePath, self.dataFileName)):
                file = open(Path(self.dataFilePath, self.dataFileName), 'r', encoding = "utf-8")
                data = json.load(file)
                for row in data:
                    self.numberOfPassword += 1
                    self.scrollAreaLayoutContents.addLayout(AppRow(data[row]["name"], data[row]["username"], data[row]["password"], data[row]["rowNumber"]))
            else:
                file = open(Path(self.dataFilePath, self.dataFileName), 'x')
                data = {}
                json.dump(data, file)
                file.close()
        else:
            makedirs(Path(self.dataFilePath))
            self.loadData()
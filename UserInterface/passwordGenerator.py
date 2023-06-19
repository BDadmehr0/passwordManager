import json
from pathlib import Path
from random import randint
from pyperclip import copy
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QPointF
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSlider,
)
from sheetStyle.darkMode import darkMode
import darkdetect


class PasswordGenerator(QWidget):
    submitClicked = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.dataFilePath = ".\\Data\\"
        self.settingFileName = ".\\setting.json"
        self.screenWidth = 1920
        self.screenHeight = 1080
        self.windowWidth = 600
        self.windowHeight = 250
        self.clockCounterVariable = 0
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.passwordLength = 20
        self.includeNumbers = True
        self.includeUppercaseCharacters = True
        self.includeLowercaseCharacters = True
        self.includeSymbols = True
        self.loadSetting()
        self.setupUi()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockCount)
        self.clock.start(10)
        self.show()

    def setupUi(self) -> None:
        if self.darkModeEnable == "Dark":
            self.setStyleSheet(darkMode)
        self.setWindowTitle("Password Generator")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(
            (self.screenWidth - self.windowWidth) // 2,
            (self.screenHeight - self.windowHeight) // 2,
            self.windowWidth,
            self.windowHeight,
        )
        self.setWindowIcon(QIcon("Assets\\password.png"))
        self.passwordManagerLayout = QVBoxLayout()
        self.header = QHBoxLayout()
        self.appNameAndIconLayout = QHBoxLayout()
        self.appIconLabel = QLabel("")
        self.appIconLabel.setPixmap(QIcon("Assets\\password.png").pixmap(QSize(16, 16)))
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
        self.minimizePushButton = QPushButton(QIcon("Assets\\minimize.png"), "")
        self.minimizePushButton.clicked.connect(self.showMinimized)
        self.appButtonsLayout.addWidget(self.minimizePushButton)
        self.maximizeOrRestoreDownPushButton = QPushButton(
            QIcon("Assets\\expand.png"), ""
        )
        self.maximizeOrRestoreDownPushButton.clicked.connect(self.maximizeOrRestore)
        self.appButtonsLayout.addWidget(self.maximizeOrRestoreDownPushButton)
        self.closePushButton = QPushButton(QIcon("Assets\\close.png"), "")
        self.closePushButton.clicked.connect(self.close)
        self.appButtonsLayout.addWidget(self.closePushButton)
        self.appButtonsLayout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.header.addLayout(self.appButtonsLayout)
        self.passwordManagerLayout.addLayout(self.header)
        self.mainAppLayout = QVBoxLayout()
        sliderLayout = QHBoxLayout()
        sliderLabel = QLabel("Password Length:", self)
        sliderLayout.addWidget(sliderLabel)
        self.sliderNumber = QLabel(" 00   ", self)
        sliderLayout.addWidget(self.sliderNumber)
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setMinimum(1)
        slider.setMaximum(50)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.setPasswordLength)
        slider.setValue(20)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(1)
        sliderLayout.addWidget(slider)
        sliderLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainAppLayout.addLayout(sliderLayout)
        checkboxLayout = QHBoxLayout()
        leftCheckboxLayout = QVBoxLayout()
        checkbox = QCheckBox("Lowercase Letters", self)
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.lowercaseToggle)
        leftCheckboxLayout.addWidget(checkbox)
        checkbox = QCheckBox("Uppercase Letters", self)
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.uppercaseToggle)
        leftCheckboxLayout.addWidget(checkbox)
        checkboxLayout.addLayout(leftCheckboxLayout)
        rightCheckboxLayout = QVBoxLayout()
        checkbox = QCheckBox("Numbers", self)
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.numbersToggle)
        rightCheckboxLayout.addWidget(checkbox)
        checkbox = QCheckBox("Symbols", self)
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(self.symbolsToggle)
        rightCheckboxLayout.addWidget(checkbox)
        checkboxLayout.addLayout(rightCheckboxLayout)
        self.mainAppLayout.addLayout(checkboxLayout)
        buttonLayout = QHBoxLayout()
        button = QPushButton("generate", self)
        button.clicked.connect(self.generatePassword)
        buttonLayout.addWidget(button)
        self.mainAppLayout.addLayout(buttonLayout)
        outputLayout = QVBoxLayout()
        self.output = QLabel("click on generate to generate your password", self)
        self.output.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        outputLayout.addWidget(self.output)
        button = QPushButton("Done", self)
        button.clicked.connect(self.submit)
        buttonLayout.addWidget(button)
        self.mainAppLayout.addLayout(outputLayout)
        self.passwordManagerLayout.addLayout(self.mainAppLayout)

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
        self.versionLabel = QLabel("V00.01.19")
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
        self.timeLabel.setText(
            "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, milliseconds)
        )

    def maximizeOrRestore(self) -> None:
        if self.isMaximized():
            self.showNormal()
            self.maximizeOrRestoreDownPushButton.setIcon(QIcon("Assets\\expand.png"))
        else:
            self.showMaximized()
            self.maximizeOrRestoreDownPushButton.setIcon(QIcon("Assets\\collapse.png"))

    def setPasswordLength(self, pl) -> None:
        self.passwordLength = pl
        self.sliderNumber.setText(" {:02d}   ".format(pl))

    def submit(self) -> None:
        self.submitClicked.emit(self.output.text())
        self.close()

    def numbersToggle(self) -> None:
        self.includeNumbers = not self.includeNumbers

    def symbolsToggle(self) -> None:
        self.includeSymbols = not self.includeSymbols

    def uppercaseToggle(self) -> None:
        self.includeUppercaseCharacters = not self.includeUppercaseCharacters

    def lowercaseToggle(self) -> None:
        self.includeLowercaseCharacters = not self.includeLowercaseCharacters

    def generatePassword(self) -> None:
        charset = []
        if self.includeNumbers:
            data = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            for i in data:
                charset.append(i)
        if self.includeUppercaseCharacters:
            data = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
            ]
            for i in data:
                charset.append(i)
        if self.includeLowercaseCharacters:
            data = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]
            for i in data:
                charset.append(i)
        if self.includeSymbols:
            data = [
                "~",
                "`",
                "!",
                "@",
                "#",
                "$",
                "%",
                "^",
                "&",
                "*",
                "(",
                ")",
                "_",
                "-",
                "+",
                "=",
                "{",
                "[",
                "]",
                "}",
                ":",
                ";",
                "'",
                '"',
                "\\",
                "|",
                "<",
                ">",
                ",",
                ".",
                "/",
                "?",
            ]
            for i in data:
                charset.append(i)
        if len(charset) == 0:
            self.output.setText(" ")
            return
        password = ""
        for j in range(self.passwordLength):
            index = randint(1, len(charset)) - 1
            password += charset[index]
        self.output.setText(password)
        copy(password)

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

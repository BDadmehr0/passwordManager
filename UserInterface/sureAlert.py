from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QPointF
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel


class SureAlert(QWidget):
    submitClicked = pyqtSignal(bool)

    def __init__(self, appVersion: str, screenWidth: int, screenHeight: int, parent=None) -> None:
        super().__init__(parent)
        self.appVersion = appVersion
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.windowWidth = 300
        self.windowHeight = 100
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
        self.show()

    def setupUi(self) -> None:
        self.setWindowTitle("Add new item")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setGeometry((self.screenWidth - self.windowWidth) // 2, (self.screenHeight - self.windowHeight) // 2, self.windowWidth, self.windowHeight)
        self.setWindowIcon(QIcon("Assets\\password.png"))
        self.alertWindowLayout = QVBoxLayout()
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
        self.alertWindowLayout.addLayout(self.header)
        self.mainAlertWindowLayout = QVBoxLayout()
        self.messageLayout = QHBoxLayout()
        self.messageLabel = QLabel("Are you sure?")
        self.messageLayout.addWidget(self.messageLabel)
        self.mainAlertWindowLayout.addLayout(self.messageLayout)
        self.ButtonsLayout = QHBoxLayout()
        self.yesButton = QPushButton("Yes")
        self.yesButton.clicked.connect(self.yes)
        self.ButtonsLayout.addWidget(self.yesButton)
        self.noButton = QPushButton("No")
        self.noButton.clicked.connect(self.no)
        self.ButtonsLayout.addWidget(self.noButton)
        self.mainAlertWindowLayout.addLayout(self.ButtonsLayout)
        self.alertWindowLayout.addLayout(self.mainAlertWindowLayout)
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
        self.alertWindowLayout.addLayout(self.footer)
        self.setLayout(self.alertWindowLayout)

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

    def yes(self) -> None:
        self.submitClicked.emit(True)
        self.closeWindow()

    def no(self) -> None:
        self.submitClicked.emit(False)
        self.closeWindow()

    def closeWindow(self) -> None:
        self.close()

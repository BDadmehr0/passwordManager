from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon
from pyperclip import copy
from UserInterface.editItem import EditItemWindow


class AppRow(QHBoxLayout):
    def __init__(self, name:str, username:str, password:str, rowNumber:int = 0):
        super().__init__()
        self.setSpacing(5)
        self.rowNumber = rowNumber
        self.nameLineEdit = QLineEdit(f"{name}")
        self.nameLineEdit.setMinimumHeight(24)
        self.nameLineEdit.setDisabled(True)
        self.addWidget(self.nameLineEdit)
        self.usernameLineEdit = QLineEdit(f"{username}")
        self.usernameLineEdit.setMinimumHeight(24)
        self.usernameLineEdit.setDisabled(True)
        self.addWidget(self.usernameLineEdit)
        self.passwordLineEdit = QLineEdit(f"{password}")
        self.passwordLineEdit.setMinimumHeight(24)
        self.passwordLineEdit.setDisabled(True)
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.addWidget(self.passwordLineEdit)
        self.hiddenOrShowButton = QPushButton(QIcon("Assets\\show.png"), "")
        self.hiddenOrShowButton.setMinimumHeight(24)
        self.hiddenOrShowButton.clicked.connect(self.hiddenOrShow)
        self.addWidget(self.hiddenOrShowButton)
        self.copyButton = QPushButton(QIcon("Assets\\copy.png"), "")
        self.copyButton.setMinimumHeight(24)
        self.copyButton.clicked.connect(self.copyPasswordToClipboard)
        self.addWidget(self.copyButton)
        self.editButton = QPushButton(QIcon("Assets\\edit.png"), "")
        self.editButton.setMinimumHeight(24)
        self.editButton.clicked.connect(self.editItemWindow)
        # TODO: build and connect the edit window
        self.addWidget(self.editButton)
        self.removeButton = QPushButton(QIcon("Assets\\remove.png"), "")
        self.removeButton.setMinimumHeight(24)
        self.removeButton.clicked.connect(self.removeRow)
        self.addWidget(self.removeButton)

    def hiddenOrShow(self) -> None:
        if self.passwordLineEdit.echoMode() == QLineEdit.EchoMode.Password:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def copyPasswordToClipboard(self) -> None:
        if self.passwordLineEdit.echoMode() == QLineEdit.EchoMode.Password:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            copy(self.passwordLineEdit.text())
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            copy(self.passwordLineEdit.text())

    def removeRow(self) -> None:
        self.removeItem(self)
        self.nameLineEdit.deleteLater()
        self.usernameLineEdit.deleteLater()
        self.passwordLineEdit.deleteLater()
        self.hiddenOrShowButton.deleteLater()
        self.copyButton.deleteLater()
        self.editButton.deleteLater()
        self.removeButton.deleteLater()
        self.deleteLater()

    def editItemWindow(self) -> None:
        self.editItemWindowUi = EditItemWindow()
        self.editItemWindowUi.nameTextEdit.setText(self.nameLineEdit.text())
        self.editItemWindowUi.usernameTextEdit.setText(self.usernameLineEdit.text())
        self.editItemWindowUi.passwordTextEdit.setText(self.passwordLineEdit.text())
        self.editItemWindowUi.submitClicked.connect(self.onEditItemWindowConfirm)

    def onEditItemWindowConfirm(self, name, username, password):
        self.nameLineEdit.setText(name)
        self.usernameLineEdit.setText(username)
        self.passwordLineEdit.setText(password)
        self.isDataChanged = True
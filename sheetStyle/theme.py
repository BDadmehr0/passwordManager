import json
from os import makedirs
from os.path import exists
from pathlib import Path

class Theme():
    def __init__(self, themeFilesPath: str, themeFileName: str) -> str:
        self.themeFilesPath = themeFilesPath
        self.themeFileName = themeFileName

    def theme(self) -> str:
        data = self.loadThemeMode()
        return self.makeThemeTemplate(data)

    def loadThemeMode(self) -> dict:
        if exists(Path(self.themeFilesPath)):
            if Path.is_file(Path(self.themeFilesPath, self.themeFileName)):
                file = open(Path(self.themeFilesPath, self.themeFileName), "r", encoding="utf-8")
                data = json.load(file)
                file.close()
                return data
            else:
                file = open(Path(self.themeFilesPath, self.themeFileName), "x")
                data = {}
                json.dump(data, file)
                file.close()
                self.loadThemeMode()
        else:
            makedirs(Path(self.themeFilesPath))
            self.loadThemeMode()

    def makeThemeTemplate(self, data: dict) -> None:
        return f"""
            QWidget {{
                background-color: {data["backgroundColor"]};
                color: {data["foregroundColor"]};
                border: none;
            }}
            QPushButton {{
                background-color: {data["backgroundColorForLightElements"]};
                border: 1px solid {data["backgroundColorForLightElements"]};
                border-radius: 4px;
                color: {data["foregroundColor"]};
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {data["backgroundColorForLightElementsOnHoverMode"]};
                border: 1px solid {data["backgroundColorForLightElementsOnHoverMode"]};
            }}
            QCheckBox {{
                color: {data["foregroundColor"]};
            }}
            QLineEdit {{
                background-color: {data["backgroundColorForLightElements"]};
                border: 1px solid {data["backgroundColorForLightElements"]};
                color: {data["foregroundColor"]};
                padding: 5px;
            }}
            QTextEdit {{
                background-color: {data["backgroundColorForLightElements"]};
                border: 1px solid {data["backgroundColorForLightElements"]};
                color: {data["foregroundColor"]};
                padding: 5px;
            }}
            QProgressBar {{
                border: 1px solid {data["backgroundColorOfScrollBars"]};
                border-radius: 7px;
                background-color: {data["backgroundColorOfTabs"]};
                text-align: center;
                font-size: 10pt;
                color: white;
            }}
            QProgressBar::chunk {{
                background-color: {data["backgroundColorOfTabsOnHoverMode"]};
                width: 5px;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: {data["backgroundColorOfTabsOnHoverMode"]};
                width: 10px;
                margin: 16px 0 16px 0;
            }}
            QScrollBar::handle:vertical {{
                background-color: {data["backgroundColorOfScrollBars"]};
                border-radius: 5px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background-color: {data["backgroundColorOfTabsOnHoverMode"]};
                height: 10px;
                margin: 0px 16px 0 16px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {data["backgroundColorOfScrollBars"]};
                border-radius: 5px;
            }}
            QTabWidget {{
                background-color: {data["backgroundColorOfTabs"]};
                border: none;
            }}
            QTabBar::tab {{
                background-color: {data["backgroundColorOfTabs"]};
                color: {data["foregroundColorOfTabs"]};
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border: none;
            }}
        
            QTabBar::tab:selected, QTabBar::tab:hover {{
                background-color: {data["backgroundColorOfTabsOnHoverMode"]};
                color: {data["foregroundColor"]};
            }}
        """
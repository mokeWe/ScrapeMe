import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QCheckBox,
    QPlainTextEdit,
)
from PyQt6.QtCore import QCoreApplication, QThread
from funcs import cog
import json
import qdarktheme
import threading


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ScrapeMe")
        self.resize(500, 400)

        # Tabs
        tabWidget = QTabWidget()
        tabWidget.addTab(Tab1(), "Scraper")
        tabWidget.addTab(Tab2(), "Settings")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)

        self.show()


class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Widgets
        self.urlLabel = QLabel("Enter URL:")
        self.resultsLabel = QLabel("Results:")
        self.textbox = QLineEdit(self)
        self.resultsBox = QPlainTextEdit(self)
        self.resultsBox.setReadOnly(True)
        self.scrapeButton = QPushButton("Scrape", self)
        self.exitButton = QPushButton("Exit", self)

        # Stylesheets
        self.resultsBox.setStyleSheet("font-family: monospace;")
        self.scrapeButton.setStyleSheet("font-weight: bold;")
        self.exitButton.setStyleSheet("color: #eb4334")

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.urlLabel, 1, 0)
        grid.addWidget(self.textbox, 1, 1)
        grid.addWidget(self.scrapeButton, 1, 2)
        grid.addWidget(self.exitButton, 4, 1)
        grid.addWidget(self.resultsLabel, 3, 0)
        grid.addWidget(self.resultsBox, 3, 1)

        self.setLayout(grid)

        # Signals
        self.scrapeButton.clicked.connect(self.scrape)
        self.exitButton.clicked.connect(self.exit)

    def scrape(self):
        self.resultsBox.clear()

        with open("settings.json", "r") as f:
            settings = json.load(f)

        url = self.textbox.text()
        if cog.Cog.ping(url):
            rawText = cog.Cog.get_html(url)
            for key, value in settings.items():
                if value:
                    locals()[key] = getattr(cog.Cog, "get_" + key)(rawText)
                    self.resultsBox.appendPlainText(key.capitalize() + ":")
                    self.resultsBox.appendPlainText(str(len(locals()[key])))

                    if len(locals()[key]) > 0:
                        cog.Cog.write_to_file(locals()[key], key)
                        self.resultsBox.appendPlainText("Saved!")

        else:
            self.resultsBox.appendPlainText("Invalid URL")

    def exit(self):
        reply = QMessageBox.question(
            self,
            "Hey!",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            QCoreApplication.quit()


class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Check if settings.json exists
    def check_settings():
        try:
            with open("settings.json", "r") as f:
                json.load(f)
        except FileNotFoundError:
            with open("settings.json", "w") as f:
                json.dump(
                    {"images": True, "links": True, "emails": True, "phones": True}, f
                )

    check_settings()

    # Definitely not the best way to do this
    def loadSettings(self):
        with open("settings.json", "r") as f:
            settings = json.load(f)
        for key, value in settings.items():
            getattr(self, key + "Box").setChecked(value)

    def initUI(self):

        # Widgets
        self.linksBox = QCheckBox("Srape links")
        self.imagesBox = QCheckBox("Srape images")
        self.emailsBox = QCheckBox("Scrape emails")
        self.phonesBox = QCheckBox("Scrape phone numbers")
        self.saveButton = QPushButton("Save", self)
        self.aboutButton = QPushButton("About", self)

        # Load settings
        self.loadSettings()

        # Signals
        self.saveButton.clicked.connect(self.save_settings)
        self.aboutButton.clicked.connect(self.about)

        # Layout
        layout = QGridLayout()
        layout.setSizeConstraint(QGridLayout.SizeConstraint.SetFixedSize)
        layout.addWidget(self.linksBox, 0, 0)
        layout.addWidget(self.imagesBox, 1, 0)
        layout.addWidget(self.emailsBox, 2, 0)
        layout.addWidget(self.phonesBox, 3, 0)
        layout.addWidget(self.saveButton, 4, 0)
        layout.addWidget(self.aboutButton, 4, 1)
        self.setLayout(layout)

    def save_settings(boxes):
        checkbox_values = {
            "images": boxes.imagesBox.isChecked(),
            "links": boxes.linksBox.isChecked(),
            "emails": boxes.emailsBox.isChecked(),
            "phones": boxes.phonesBox.isChecked(),
        }
        with open("settings.json", "w") as f:
            json.dump(checkbox_values, f)

    def about(self):
        QMessageBox.about(
            self,
            "ScrapeMe v1.1",
            "A basic web scraper made with Python and PyQt5.\n\nhttps://github.com/mokeWe/ScrapeMe",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    ex = App()
    sys.exit(app.exec())

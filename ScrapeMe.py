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
from PyQt6.QtCore import QCoreApplication
from funcs import cog
from configparser import ConfigParser
import qdarktheme


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
        gaw = lambda w, r, c: grid.addWidget(w, r, c)
        gaw(self.urlLabel, 1, 0)
        gaw(self.textbox, 1, 1)
        gaw(self.scrapeButton, 1, 2)
        gaw(self.exitButton, 4, 1)
        gaw(self.resultsLabel, 3, 0)
        gaw(self.resultsBox, 3, 1)
        self.setLayout(grid)

        # Signals
        self.scrapeButton.clicked.connect(self.scrape)
        self.exitButton.clicked.connect(self.exit)

    def scrape(self):
        self.resultsBox.clear()
        settings = ConfigParser()
        settings.read("settings.ini")
        url = self.textbox.text()

        if cog.Cog.ping(url):
            rawText = cog.Cog.get_html(url)
            for setting in settings["settings"]:
                if settings.getboolean("settings", setting):
                    lenset = getattr(cog.Cog, "get_" + setting)(rawText)
                    self.resultsBox.appendPlainText(setting.capitalize() + ":")
                    self.resultsBox.appendPlainText(str(len(lenset)))

                    if len(lenset) > 0:
                        cog.Cog.write_to_file(lenset, setting)
                        self.resultsBox.appendPlainText("Saved!\n")
                    else:
                        self.resultsBox.appendPlainText("Nothing to save.\n")
        else:
            self.resultsBox.appendPlainText("Error: Invalid URL")

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

    def check_settings():
        config = ConfigParser()
        config.read("settings.ini")
        if not config.has_section("settings"):
            config.add_section("settings")
            config.set("settings", "links", "True")
            config.set("settings", "images", "True")
            config.set("settings", "emails", "True")
            config.set("settings", "phones", "True")
            with open("settings.ini", "w") as f:
                config.write(f)
            print("settings.ini created")
        else:
            print("settings.ini exists")

    check_settings()

    def saveSettings(self):
        config = ConfigParser()
        config.read("settings.ini")
        config.set("settings", "links", str(self.linksBox.isChecked()))
        config.set("settings", "images", str(self.imagesBox.isChecked()))
        config.set("settings", "emails", str(self.emailsBox.isChecked()))
        config.set("settings", "phones", str(self.phonesBox.isChecked()))
        with open("settings.ini", "w") as f:
            config.write(f)

    def loadSettings(self):
        config = ConfigParser()
        config.read("settings.ini")
        self.linksBox.setChecked(config.getboolean("settings", "links"))
        self.imagesBox.setChecked(config.getboolean("settings", "images"))
        self.emailsBox.setChecked(config.getboolean("settings", "emails"))
        self.phonesBox.setChecked(config.getboolean("settings", "phones"))

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
        self.saveButton.clicked.connect(self.saveSettings)
        self.aboutButton.clicked.connect(self.about)

        # Layout
        layout = QGridLayout()
        law = lambda w, r, c: layout.addWidget(w, r, c)
        law(self.linksBox, 0, 0)
        law(self.imagesBox, 1, 0)
        law(self.emailsBox, 2, 0)
        law(self.phonesBox, 3, 0)
        law(self.saveButton, 4, 0)
        law(self.aboutButton, 4, 1)
        self.setLayout(layout)

    def about(self):
        QMessageBox.about(
            self,
            "ScrapeMe",
            "A basic web scraper made with Python and PyQt5.\n\nhttps://github.com/mokeWe/ScrapeMe",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    ex = App()
    sys.exit(app.exec())

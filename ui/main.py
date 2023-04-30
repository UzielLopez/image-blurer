import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from Pages.MainPage import MainApp
from Pages.ResultPage import ResultPage
from Utils.index import getAllImages


if __name__ == "__main__":
    app = QApplication(sys.argv)

    results = False

    resultsPage = ResultPage("images/blur/f5.bmp")
    configPage = MainApp(resultsPage)

    configPage.show()

    timer = QTimer()
    timer.timeout.connect(lambda: getAllImages(
        "images/blur", resultsPage))
    timer.start(5000)

    sys.exit(app.exec_())

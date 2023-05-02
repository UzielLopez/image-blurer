import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from Pages.MainPage import MainApp
from Pages.ResultPage import ResultPage
from Utils.index import getAllImages


if __name__ == "__main__":
    app = QApplication(sys.argv)

    results = False

    imagePath = [""]

    resultsPage = ResultPage("")
    configPage = MainApp(resultsPage, imagePath)

    configPage.show()

    timer = QTimer()
    timer.timeout.connect(lambda: getAllImages(
        imagePath[0], resultsPage))
    timer.start(5000)

    sys.exit(app.exec_())

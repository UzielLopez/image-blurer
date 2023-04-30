import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from Pages.MainPage import MainApp
from Utils.index import getAllImages

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = MainApp(
        "images/blur/f5.bmp")

    timer = QTimer()
    timer.timeout.connect(lambda: getAllImages(
        "images/blur", demo))
    timer.start(10000)

    demo.show()
    sys.exit(app.exec_())

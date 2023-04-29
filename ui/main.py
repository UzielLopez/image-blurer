import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from PIL import Image

from Pages.MainPage import MainApp


def getAllImages(imagesPath: str, app: MainApp):
    if len(app.images) >= 40:
        print("Ya se han cargado todas las imagenes")
        return

    images = []
    for file in os.listdir(imagesPath):
        if file.endswith(".bmp"):
            try:
                imagePath = imagesPath + "/" + file
                image = Image.open(imagePath)

                if imagesPath not in app.images:
                    images.append(imagePath)
                    print("Añadiendo: " + imagePath)
                else:
                    print("La imagen ya se ha añadido a la app")
            except:
                print(file + " la imagen aun se encuentra en construcción")

    images = sorted(images, key=lambda x: x[-2:])
    app.images.extend(images)
    app.evaluateButtonsEnable()
    print("--------------------")


def test():
    print("test")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = MainApp("images/blur/f5.bmp")

    timer = QTimer()
    timer.timeout.connect(lambda: getAllImages("images/blur", demo))
    timer.start(10000)

    demo.show()
    sys.exit(app.exec_())

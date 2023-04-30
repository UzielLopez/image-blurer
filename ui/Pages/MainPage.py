from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QMainWindow, QHBoxLayout
import sys

from Widgets.ImageLabel import ImageLabel
from Widgets.CustomButton import CustomButton


class MainApp(QMainWindow):
    def __init__(self, baseImage):
        super().__init__()
        # cargando el diseño desde el archivo .ui
        loadUi('diseño.ui', self)

        self.currentImageIndex = 0
        self.images = [baseImage]

        self.photoViewer = ImageLabel("Arrastra aquí tu imagen")
        self.verticalLayout.addWidget(self.photoViewer)

        self.mainImageLabel = self.createLabelForImages()
        self.verticalLayout.addWidget(self.mainImageLabel)

        self.imageTitleLabel = QLabel(self.images[self.currentImageIndex])
        self.verticalLayout.addWidget(self.imageTitleLabel)

        self.prevButton = CustomButton(
            QIcon("images/icons/prev.png"), "Ver la imagen anterior", "PREV", self.clickChangeImage)
        self.prevButton.setDisabled(True)

        self.nextButton = CustomButton(
            QIcon("images/icons/next.png"), "Ver la imagen siguiente", "NEXT", self.clickChangeImage)
        self.nextButton.setDisabled(True)

        buttonsWidget = self.createButtonGroup()
        self.verticalLayout.addWidget(buttonsWidget)

        self.setAcceptDrops(True)

        self.pushButton.clicked.connect(self.on_button_click)

    def evaluateButtonsEnable(self):
        if self.currentImageIndex < len(self.images)-1:
            self.nextButton.setDisabled(False)
        else:
            self.nextButton.setDisabled(True)

        if self.currentImageIndex > 0:
            self.prevButton.setDisabled(False)
        else:
            self.prevButton.setDisabled(True)

    def clickChangeImage(self, button: CustomButton):
        modifier = 1 if button.type == "NEXT" else -1
        self.currentImageIndex += modifier
        self.evaluateButtonsEnable()

        if (self.currentImageIndex > 0 and self.currentImageIndex < len(self.images)):
            self.changePixelmapMainImage(self.images[self.currentImageIndex])
            self.imageTitleLabel.setText(self.images[self.currentImageIndex])
            return

    def changePixelmapMainImage(self, imagePath: str):
        newMainImage = QPixmap(imagePath)
        newMainImage = newMainImage.scaled(320, 240)
        self.mainImageLabel.setPixmap(newMainImage)

    def createButtonGroup(self) -> QWidget:
        buttonsWidget = QWidget()
        buttonsLayout = QHBoxLayout(buttonsWidget)
        buttonsLayout.addWidget(self.prevButton)
        buttonsLayout.addWidget(self.nextButton)

        return buttonsWidget

    def createLabelForImages(self) -> QLabel:
        mainImageLabel = ImageLabel("", "MAIN")
        # Creamos la imagen proporcionando su ruta.
        mainImage = QPixmap(self.images[self.currentImageIndex])
        # La escalamos para presentarla en pantalla.
        mainImage = mainImage.scaled(320, 240)
        # Le colocamos al label la imagen creada.
        mainImageLabel.setPixmap(mainImage)

        return mainImageLabel

    def on_button_click(self):
        self.photoViewer.setText('\n\n Button Clicked \n\n')

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

    def getImage(self, ) -> QWidget:
        imageWidget = QWidget()
        imageWidget.resize(640, 480)
        imageWidget.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        return imageWidget

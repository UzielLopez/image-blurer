from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton

from Widgets.ImageLabel import ImageLabel


class MainApp(QMainWindow):
    def __init__(self, results):
        super().__init__()
        # cargando el diseño desde el archivo .ui
        loadUi('diseño.ui', self)

        self.currentImageIndex = 0
        self.photoViewer = ImageLabel("Arrastra aquí tu imagen")
        self.verticalLayout.addWidget(self.photoViewer)

        self.setAcceptDrops(True)

        self.pushButton.clicked.connect(self.on_button_click)

        self.getResultsButton = QPushButton("Obtener resultados")
        self.getResultsButton.clicked.connect(lambda x: results.show())

        self.verticalLayout.addWidget(self.getResultsButton)

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

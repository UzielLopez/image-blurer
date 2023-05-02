from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QTextEdit, QLabel

from Widgets.ImageLabel import ImageLabel


class MainApp(QMainWindow):
    def __init__(self, resultsPage, imagePath):
        super().__init__()
        # cargando el diseño desde el archivo .ui
        loadUi('diseño.ui', self)

        self.currentImageIndex = 0
        self.photoViewer = ImageLabel("Arrastra aquí tu imagen")
        self.verticalLayout.addWidget(self.photoViewer)
        self.photoViewer.setAlignment(Qt.AlignCenter)
        self.photoViewer.setScaledContents(True)

        self.setAcceptDrops(True)

        self.warningLabel = self.findChild(QLabel, 'warning_1')
        self.warningLabel = self.findChild(QLabel, 'warning_2')
        self.ejecutar.clicked.connect(self.validator)

        self.getResultsButton = QPushButton("Obtener resultados")
        self.getResultsButton.clicked.connect(lambda x : self.results_click(resultsPage, imagePath))

        self.verticalLayout.addWidget(self.getResultsButton)

    def results_click(self, resultsPage, imagePath): 
        imagePath[0] = "images/blur"
        resultsPage.show()

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
        self.image_path = file_path
    
    def validator(self):
        text = self.textEdit.toPlainText()
        if not text:
            self.warning_1.setText("Ingrese un número entero \nentre el 3 y el 17")
        else:
            try:
                value = int(text)
                if 3 <= value <= 17:
                    self.warning_1.setText("Óptimo")
                else:
                    self.warning_1.setText("Ingrese un número entero válido")
            except ValueError:
                self.warning_1.setText("El número debe estar en el \nrango del 3 al 17")
        
        text2 = self.textEdit_2.toPlainText()
        if not text2:
            self.warning_2.setText("Ingrese un número entero \nentre el 1 y el 50")
        else:
            try:
                value = int(text2)
                if 1 <= value <= 50:
                    self.warning_2.setText("Óptimo")
                else:
                    self.warning_2.setText("Ingrese un número entero válido")
            except ValueError:
                self.warning_2.setText("El número debe estar en el \nrango del 1 al 50")

    def getImage(self, ) -> QWidget:
        imageWidget = QWidget()
        imageWidget.resize(640, 480)
        imageWidget.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        return imageWidget
import sys, os, glob
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('diseño.ui', self)  # cargando el diseño desde el archivo .ui

        # Obtener el QLabel del archivo .ui y asignarlo a self.photoViewer
        self.photoViewer = self.findChild(QLabel, "drop")
        self.photoViewer.setAlignment(Qt.AlignCenter)
        self.photoViewer.setScaledContents(True)

        self.setAcceptDrops(True)

        #self.pushButton.clicked.connect(self.on_button_click)

        # Inicializar la lista de imágenes y el índice actual
        self.image_list = sorted(glob.glob('C:/Users/ref2k/OneDrive/Escritorio/imagen/imagen*.png'))
        self.current_image_index = 0

        # Conectar las señales de los botones a las funciones correspondientes
        self.prevButton.clicked.connect(self.show_previous_image)
        self.nextButton.clicked.connect(self.show_next_image)

        # Mostrar la primera imagen
        self.show_image()

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

    def show_image(self):
        # Obtener la ruta de la imagen actual
        current_image_path = self.image_list[self.current_image_index]

        # Cargar la imagen en un QPixmap
        pixmap = QPixmap(current_image_path)

        # Ajustar la imagen a la etiqueta
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation))

        # Mostrar el nombre del archivo actual en el QLabel
        self.filename_label.setText(os.path.basename(current_image_path))

    def show_previous_image(self):
        # Disminuir el índice actual y mostrar la imagen correspondiente
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.image_list) - 1
        self.show_image()

    def show_next_image(self):
        # Aumentar el índice actual y mostrar la imagen correspondiente
        self.current_image_index += 1
        if self.current_image_index >= len(self.image_list):
            self.current_image_index = 0
        self.show_image()


if __name__ == '__main__':
    # Crear la aplicación y la ventana principal
    app = QApplication([])
    window = AppDemo()
    window.show()
    app.exec_()
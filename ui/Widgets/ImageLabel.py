from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(self, text="", type="DRAG"):
        super().__init__()
        self.type = type
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n{}\n\n'.format(text))

        if (type == "DRAG"):
            self.setStyleSheet('''
                QLabel{
                    border: 4px dashed #aaa
                }
            ''')

    def setPixmap(self, image):
        super().setPixmap(image)
        if self.type == "MAIN":
            self.resize(image.width(), image.height())

import os
import os.path
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class CustomButton(QPushButton):
    def __init__(self, icon: QIcon, tooltip: str, type: str, changeImage):
        super().__init__(icon, "")

        self.changeImageFunction = changeImage
        self.type = type
        self.setToolTip(tooltip)
        self.setGeometry(200, 150, 100, 40)
        self.clicked.connect(self.on_Click)

    def on_Click(self):
        self.changeImageFunction(self)

    def imageEvaluator(self):
        for file in os.listdir(self.path):
            if file.endswith(".bmp"):
                print("nice")

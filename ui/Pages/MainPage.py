import subprocess
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QTextEdit, QLabel

from Widgets.ImageLabel import ImageLabel
from Utils.c_integration import check_cluster_status

class BlurringWorker(QThread):
    output = pyqtSignal(str, name="blurring_result")
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.pipe = None
        self.image_path = ""
        self.output_path = ""
        self.initial_mask = 3
        self.exiting = False
    
    def __del__(self):
        self.exiting = True
        self.wait()

    def stop(self):
        self.terminate()
        if self.pipe != None:
            self.pipe.kill()

    def blur(self, image_path: str, initial_mask: int, output_path: str):
        self.image_path = image_path
        self.initial_mask = initial_mask
        self.output_path = output_path
        self.start()

    def run(self):
        command_arguments = f"-f {self.image_path} -m {self.initial_mask} -d {self.output_path}"
        #blurring_command = f"/home/uziel/Universidad/Redes/cm/image-blurer/a.out " + command_arguments
        hostfile = "/mirror/mpiu/machinefile" # TODO: change depending on relative path
        blurring_executable = "/mirror/mpiu/blur" # TODO: change depending on relative path and executable name
        mpi_blurring_command = f"mpirun -hostfile {hostfile} {blurring_executable} " + command_arguments
        print("Se ejecutaría el comando desde el worker: ", mpi_blurring_command)
        #print("se va a ejecutar el comando desde el worker: ", blurring_command)
        #self.pipe = subprocess.Popen("exec " + mpi_blurring_command, shell=True, stdout=subprocess.PIPE)
        self.pipe = subprocess.Popen("exec " + mpi_blurring_command, shell=True, stdout=subprocess.PIPE)
        blurring_result = self.pipe.communicate()[0].decode("utf-8")
        self.output.emit(blurring_result)

class MainApp(QMainWindow):
    def __init__(self, resultsPage, imagePath):
        super().__init__()
        self.blurringThread = BlurringWorker()
        # cargando el diseño desde el archivo .ui
        loadUi('diseño.ui', self)

        self.currentImageIndex = 0
        self.image_path = ""
        self.executing_blurring = False
        self.available_nodes = 0

        self.blurringThread.finished.connect(self.reset_ui)
        self.blurringThread.output[str].connect(self._debug_output)

        self.photoViewer = ImageLabel("Arrastra aquí tu imagen")
        self.verticalLayout.addWidget(self.photoViewer)
        self.photoViewer.setAlignment(Qt.AlignCenter)
        self.photoViewer.setScaledContents(True)

        self.setAcceptDrops(True)

        self.warningLabel = self.findChild(QLabel, 'warning_1')
        self.warningLabel = self.findChild(QLabel, 'warning_2')

        self.ejecutar.clicked.connect(self.validator)
        self.ejecutar.setEnabled(False)

        self.getResultsButton = QPushButton("Obtener resultados")
        self.getResultsButton.clicked.connect(lambda x : self.results_click(resultsPage, imagePath))

        self.verticalLayout.addWidget(self.getResultsButton)

    def results_click(self, resultsPage, imagePath): 
        imagePath[0] = self.textEdit_3.toPlainText()
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
        self.ejecutar.setEnabled(True)

    def reset_ui(self):
        self.executing_blurring = False
        self.ejecutar.setText("Ejecutar")
    
    def validator(self):

        if self.executing_blurring:
            self.blurringThread.stop()
            return

        initial_mask = self.textEdit.toPlainText()
        valid_initial_mask = False
        if not initial_mask:
            self.warning_1.setText("Ingrese un número entero \nentre el 3 y el 17")
        else:
            try:
                value = int(initial_mask)
                if 3 <= value <= 17:
                    self.warning_1.setText("Óptimo")
                    valid_initial_mask = True
                else:
                    self.warning_1.setText("Ingrese un número entero válido")
            except ValueError:
                self.warning_1.setText("El número debe estar en el \nrango del 3 al 17")
        
        number_of_masks = self.textEdit_2.toPlainText()
        valid_number_of_masks = False
        if not number_of_masks:
            self.warning_2.setText("Ingrese un número entero \nentre el 1 y el 50")
        else:
            try:
                value = int(number_of_masks)
                if 1 <= value <= 50:
                    self.warning_2.setText("Óptimo")
                    valid_number_of_masks = True
                else:
                    self.warning_2.setText("Ingrese un número entero válido")
            except ValueError:
                self.warning_2.setText("El número debe estar en el \nrango del 1 al 50")

        if valid_initial_mask and valid_number_of_masks:
            output_path = self.textEdit_3.toPlainText()
            if not output_path.endswith('/'):
                output_path += '/'
            self.execute_blurring(int(initial_mask), int(number_of_masks), output_path)

    def getImage(self, ) -> QWidget:
        imageWidget = QWidget()
        imageWidget.resize(640, 480)
        imageWidget.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        return imageWidget
    
    def _debug_output(self, output):
        print("Acabó el blurring!!!")
        print("Output: ")
        print(output)

    def execute_blurring(self, initial_mask: int, number_of_masks: int, output_path: str):

        self.ejecutar.setEnabled(False)
        # Antes de ejecutar, creamos el nuevo machinefile dependiendo del estado de la red
        self.available_nodes = check_cluster_status(number_of_masks)

        # TODO: cuando haya no haya ni un solo nodo disponible (que sería el caso donde la config este mal)
        # decirle al usuario que no se va a ejecutar (?)
        if self.available_nodes == 0:
            print("No hay nodos disponibles. Revisa la configuración del clúster.")
            self.ejecutar.setEnabled(True)
            return
        
        self.label_3.setText(f"Nodos disponibles: {self.available_nodes}")
        
        print(f"Se distribuirá el trabajo entre {self.available_nodes} nodos")
        self.ejecutar.setText("Cancelar")
        self.executing_blurring = True
        self.ejecutar.setEnabled(True)
        
        self.blurringThread.blur(self.image_path, initial_mask, output_path)

        

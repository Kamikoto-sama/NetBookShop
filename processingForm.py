from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui.convertedUi.processingForm import Ui_processingForm

class ProcessingForm(Ui_processingForm, QWidget):
    def __init__(self, parent):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModal)

    def hide(self):
        self.close()

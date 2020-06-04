from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui.convertedUi.processingForm import Ui_processingForm

class ProcessingForm(Ui_processingForm, QWidget):
	def __init__(self, parent):
		super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
		self.setupUi(self)
		self.setWindowModality(Qt.WindowModal)
		self.statusBar.hide()
		self.message.hide()
		
	def showRequestProcessing(self):
		self.message.show()
		messageText = "Processing request..."
		self.message.setText(messageText)
		self.show()
		
	def hide(self):
		self.message.hide()
		self.statusBar.hide()
		self.close()
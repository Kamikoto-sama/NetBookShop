from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget

from ui.convertedUi.processingForm import Ui_processingForm

class ProcessingForm(Ui_processingForm, QWidget):
	updateStatus = pyqtSignal(str, int)
	def __init__(self, parent):
		super().__init__(parent, Qt.Window | Qt.FramelessWindowHint)
		self.setupUi(self)
		self.setWindowModality(Qt.WindowModal)
		self.statusBar.hide()
		self.message.hide()
		self.updateStatus.connect(self.__updateStatus)
		
	def showRequestProcessing(self):
		self.message.show()
		messageText = "Processing request..."
		self.message.setText(messageText)
		self.show()
		
	def showWithStatus(self, statusText: str, maxValue: int):
		self.statusBar.show()
		self.statusBar.setFormat(statusText)
		self.statusBar.setMaximum(maxValue)
		self.statusBar.setValue(0)
		self.show()
		
	def __updateStatus(self, statusText, value):
		self.statusBar.setFormat(statusText)
		self.statusBar.setValue(value)
		
	def hide(self):
		self.message.hide()
		self.statusBar.hide()
		self.close()
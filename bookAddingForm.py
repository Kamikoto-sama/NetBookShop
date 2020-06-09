from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from clientWorker import ClientWorker
from processingForm import ProcessingForm
from ui.convertedUi.bookAddingForm import Ui_bookAddingForm

class BookAddingForm(QWidget, Ui_bookAddingForm):
	def __init__(self, parent, clientWorker: ClientWorker):
		super().__init__(parent, Qt.WindowCloseButtonHint | Qt.Window)
		self.setupUi(self)
		self.setWindowModality(Qt.WindowModal)
		self.addBtn.clicked.connect(self.addBook)
		self.clientWorker = clientWorker
		self.processingForm = ProcessingForm(self)
		
	def init(self, authorsNames, publishersNames):
		
		
	def addBook(self):
		self.processingForm.show()
		
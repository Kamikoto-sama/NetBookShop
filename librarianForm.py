from PyQt5.QtWidgets import QWidget

from clientWorker import ClientWorker
from ui.convertedUi.librarianForm import Ui_librarianForm

class LibrarianForm(Ui_librarianForm, QWidget):
	def __init__(self, clientWorker: ClientWorker):
		super().__init__()
		self.setupUi(self)
		self.clientWorker = clientWorker
		
	def init(self):
		self.show()
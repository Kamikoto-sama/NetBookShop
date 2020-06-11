from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox

from requestBuilder import RequestBuilder
from ui.convertedUi.authorAddingForm import Ui_authorAddingForm

class AuthorAddingForm(QWidget, Ui_authorAddingForm):
	def __init__(self, parent):
		super().__init__(parent, Qt.WindowCloseButtonHint | Qt.Window)
		self.setupUi(self)
		self.setWindowModality(Qt.WindowModal)
		self.addBtn.clicked.connect(self.addAuthor)
		self.parent = parent

	def addAuthor(self):
		if self.nameEdit.text() == "":
			QMessageBox.warning(self, "Invalid input", "Name is required")
			return
		authorData = {
			"name" : self.nameEdit.text(),
			"birthDate": self.dateEdit.text(),
			"bio": self.bioEdit.toPlainText()
		}
		request = RequestBuilder.Librarian.addAuthor(authorData)
		self.parent.processingTableName = "authors"
		handleRes = lambda res: self.parent.itemAddedEvent.emit(res)
		self.parent.clientWorker.requestData(request, handleRes)

		self.close()
		self.parent.processingForm.show()
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox

from requestBuilder import RequestBuilder
from ui.convertedUi.publisherAddingForm import Ui_publisherAddingForm

class PublisherAddingForm(QWidget, Ui_publisherAddingForm):
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
		publisherData = {
			"name" : self.nameEdit.text(),
			"creationDate": self.dateEdit.text(),
		}
		request = RequestBuilder.Librarian.addPublisher(publisherData)
		self.parent.processingTableName = "publishers"
		handleRes = lambda res: self.parent.itemAddedEvent.emit(res)
		self.parent.clientWorker.requestData(request, handleRes)

		self.close()
		self.parent.processingForm.show()
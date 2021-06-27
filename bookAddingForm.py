from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox

from requestBuilder import RequestBuilder
from ui.convertedUi.bookAddingForm import Ui_bookAddingForm

class BookAddingForm(QWidget, Ui_bookAddingForm):
    def __init__(self, parent):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.Window)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModal)
        self.addBtn.clicked.connect(self.addBook)
        self.parent = parent

    def fillLists(self, authorsNames, publishersNames):
        self.authorsList.addItems(authorsNames)
        self.publishersList.addItems(publishersNames)

    def addBook(self):
        if not self.validateInput():
            return
        bookData = {
            "name": self.nameEdit.text(),
            "genre": self.genreEdit.text(),
            "pageCount": self.pageCountEdit.text(),
            "author": self.authorsList.currentText(),
            "publisher": self.publishersList.currentText(),
            "count": self.countEdit.text(),
            "price": self.priceEdit.text(),
        }
        request = RequestBuilder.Librarian.addBook(bookData)
        self.parent.processingTableName = "books"
        handleRes = lambda res: self.parent.itemAddedEvent.emit(res)
        self.parent.clientWorker.requestData(request, handleRes)

        self.close()
        self.parent.processingForm.show()

    def validateInput(self):
        inputValues = [
            self.nameEdit.text(),
            self.genreEdit.text(),
            self.authorsList.currentText(),
            self.publishersList.currentText()
        ]
        if "" not in inputValues:
            return True
        QMessageBox.warning(self, "Invalid input", "All fields are required")
        return False

    def closeEvent(self, event: QCloseEvent):
        self.authorsList.clear()
        self.publishersList.clear()
        event.accept()

from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem

from clientWorker import ClientWorker
from models import Response
from requestBuilder import RequestBuilder
from ui.convertedUi.customerForm import Ui_customerForm

class CustomerForm(Ui_customerForm, QWidget):
	initialDataReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()
	def __init__(self, clientWorker: ClientWorker):
		super().__init__()
		self.setupUi(self)
		self.clientWorker = clientWorker
		self.initialDataReceivedEvent.connect(self.initBooksPage)
		self.serverConnectionLostEvent.connect(self.onServerConnectionLost)
		
	def init(self):
		self.show()
		Thread(target=self.requestInitData).start()
		
	def requestInitData(self):
		handleInitialData = lambda data: self.initialDataReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getBooksPageData()
		self.clientWorker.requestData(request, handleInitialData)
		
	def initBooksPage(self, response: Response):
		if not response.succeed:
			QMessageBox().critical(self, "Loading data error", response.message)
			self.close()
			return
		self.authorsList.addItems(response.body["authorsNames"])
		self.publishersList.addItems(response.body["publishersNames"])
		self.fillBooksTable(response.body["books"])
		
	def fillBooksTable(self, books: list):
		self.booksTable.setRowCount(len(books))
		for rowIndex, book in enumerate(books):
			for colIndex, colName in enumerate(book):
				if colName == "id":
					continue
				item = QTableWidgetItem(str(book[colName]))
				item.setTextAlignment(Qt.AlignCenter)
				self.booksTable.setItem(rowIndex, colIndex - 1, item)
			
	def onServerConnectionLost(self):
		QMessageBox.critical(self, "Error", "Server connection lost")
		self.close()
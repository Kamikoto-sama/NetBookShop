from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem

from clientWorker import ClientWorker
from models import Response
from requestBuilder import RequestBuilder
from ui.convertedUi.customerForm import Ui_customerForm

class CustomerForm(Ui_customerForm, QWidget):
	initialDataReceivedEvent = pyqtSignal(object)
	ordersReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()
	def __init__(self, clientWorker: ClientWorker):
		super().__init__()
		self.setupUi(self)
		self.clientWorker = clientWorker
		self.initialDataReceivedEvent.connect(self.initBooksPage)
		self.serverConnectionLostEvent.connect(self.onServerConnectionLost)
		self.ordersReceivedEvent.connect(self.initOrdersPage)
		
		self.tabs.currentChanged.connect(self.onCurrentTabChanged)
		self.ordersTabLoaded = False
		
	def init(self):
		self.show()
		Thread(target=self.requestInitData).start()
		
	def requestInitData(self):
		handleInitialData = lambda data: self.initialDataReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getBooksPageData()
		self.clientWorker.requestData(request, handleInitialData)
		
	def initBooksPage(self, response: Response):
		if not response.succeed:
			self.onResponseError("Loading data error", response.message)
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
				
	def onCurrentTabChanged(self, index):
		if index == 0 or self.ordersTabLoaded:
			return
		self.ordersTabLoaded = True
		handleResponse = lambda data: self.ordersReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getOrders()
		self.clientWorker.requestData(request, handleResponse)
		
	def initOrdersPage(self, response: Response):
		if not response.succeed:
			self.onResponseError("User orders fetch error", response.message)
			return
		self.fillOrdersTable(response.body)
		
	def fillOrdersTable(self, orders: list):
		self.ordersTable.setRowCount(len(orders))
		for rowIndex, order in enumerate(orders):
			for colIndex, colName in enumerate(order):
				if colName == "id":
					continue
				item = QTableWidgetItem(str(order[colName]))
				item.setTextAlignment(Qt.AlignCenter)
				self.ordersTable.setItem(rowIndex, colIndex - 1, item)
		
	def onServerConnectionLost(self):
		QMessageBox.critical(self, "Error", "Server connection lost")
		self.close()
		
	def onResponseError(self, title, message):
		QMessageBox().critical(self, title, message)
		self.close()
from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QTableWidget

from clientWorker import ClientWorker
from models import Response, ChangesUpdateEvent
from requestBuilder import RequestBuilder
from ui.convertedUi.customerForm import Ui_customerForm

class CustomerForm(Ui_customerForm, QWidget):
	initialDataReceivedEvent = pyqtSignal(object)
	ordersReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()
	changesReceivedEvent = pyqtSignal(object)
	orderMadeEvent = pyqtSignal(object)
	def __init__(self, clientWorker: ClientWorker):
		super().__init__()
		self.setupUi(self)
		self.clientWorker = clientWorker
		self.initialDataReceivedEvent.connect(self.initBooksPage)
		self.serverConnectionLostEvent.connect(self.onServerConnectionLost)
		clientWorker.onServerDisconnected = lambda: self.serverConnectionLostEvent.emit()
		self.ordersReceivedEvent.connect(self.initOrdersPage)
		self.changesReceivedEvent.connect(self.onChangesReceived)
		self.orderMadeEvent.connect(self.onOrderMade)
		
		self.tabs.currentChanged.connect(self.onCurrentTabChanged)
		self.ordersTabLoaded = False
		self.itemsMap = {
			"orders":[],
			"books":[]
		}
		
		self.orderBtn.clicked.connect(self.makeOrder)
		
	def onOrderMade(self, response):
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return
		print(response.body)
		
	def onChangesReceived(self, changesUpdate: ChangesUpdateEvent):
		tables = ", ".join(changesUpdate.tables)
		title = "Changes update"
		message = f"Some data has changed in: {tables}\n Do you want to update tables?"
		buttons = QMessageBox.Yes | QMessageBox.No
		res = QMessageBox().information(self, title, message, buttons, QMessageBox.No)
		print(res)
		
	def makeOrder(self):
		rowIndex = self.booksTable.currentRow()
		if rowIndex < 0:
			return
		booksCount = int(self.booksTable.item(rowIndex, 5).text())
		if booksCount == 0:
			self.showInvalidOperationMessage("There is no books left")
			return 
		bookId = self.itemsMap["books"][rowIndex]
		request = RequestBuilder.Customer.makeOrder(bookId)
		responseHandler = lambda data: self.orderMadeEvent.emit(data)
		self.clientWorker.requestData(request, responseHandler)
		
	def init(self):
		self.show()
		Thread(target=self.requestInitData).start()
		
	def requestInitData(self):
		handleInitialData = lambda data: self.initialDataReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getBooksPageData()
		self.clientWorker.requestData(request, handleInitialData)
		
	def initBooksPage(self, response: Response):
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return
		self.authorsList.addItems(response.body["authorsNames"])
		self.publishersList.addItems(response.body["publishersNames"])
		self.fillTable(self.booksTable, response.body["books"], "books")
				
	def onCurrentTabChanged(self, index):
		if index == 0 or self.ordersTabLoaded:
			return
		self.ordersTabLoaded = True
		handleResponse = lambda data: self.ordersReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getOrders()
		self.clientWorker.requestData(request, handleResponse)
		
	def initOrdersPage(self, response: Response):
		if not response.succeed:
			self.showErrorMessage("User orders fetch error", response.message)
			return
		self.fillTable(self.ordersTable, response.body, "orders")
		
	def fillTable(self, tableWidget: QTableWidget, items, tableName):
		tableWidget.setRowCount(len(items))
		for rowIndex, item in enumerate(items):
			for colIndex, colName in enumerate(item):
				if colName == "id":
					self.itemsMap[tableName].append(item[colName])
					continue
				cell = QTableWidgetItem(str(item[colName]))
				cell.setTextAlignment(Qt.AlignCenter)
				tableWidget.setItem(rowIndex, colIndex - 1, cell)
		
	def onServerConnectionLost(self):
		QMessageBox.critical(self, "Error", "Server connection lost")
		self.close()
		
	def showInvalidOperationMessage(self, message):
		QMessageBox().warning(self, "Invalid operation", message)

	def showErrorMessage(self, title, message):
		QMessageBox().critical(self, title, message)
		self.close()
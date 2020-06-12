from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QTableWidget, QHeaderView

from authorAddingForm import AuthorAddingForm
from clientWorker import ClientWorker
from models import Response, ChangesEvent
from processingForm import ProcessingForm
from publisherAddingForm import PublisherAddingForm
from requestBuilder import RequestBuilder
from ui.convertedUi.customerForm import Ui_customerForm

class CustomerForm(Ui_customerForm, QWidget):
	initialDataReceivedEvent = pyqtSignal(object)
	ordersReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()
	changesReceivedEvent = pyqtSignal(object)
	orderMadeEvent = pyqtSignal(object)
	orderCanceledEvent = pyqtSignal(object)
	filteredBooksReceivedEvent = pyqtSignal(object)
	itemInfoReceivedEvent = pyqtSignal(object)
	def __init__(self, clientWorker: ClientWorker):
		super().__init__(None, Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.setupUi(self)
		
		self.clientWorker = clientWorker
		self.initialDataReceivedEvent.connect(self.initBooksPage)
		self.serverConnectionLostEvent.connect(self.onServerConnectionLost)
		clientWorker.onServerDisconnected = lambda: self.serverConnectionLostEvent.emit()
		self.ordersReceivedEvent.connect(self.initOrdersPage)
		self.changesReceivedEvent.connect(self.onChangesReceived)
		clientWorker.onChangesReceived = lambda data: self.changesReceivedEvent.emit(data)
		self.orderMadeEvent.connect(self.onOrderMade)
		
		self.tabs.currentChanged.connect(self.onCurrentTabChanged)
		self.ordersTabLoaded = False
		self.itemsMap = {
			"orders":[],
			"books":[]
		}
		self.requestedItemInfo = None
		
		self.orderBtn.clicked.connect(self.makeOrder)
		self.processingForm = ProcessingForm(self)
		self.orderCanceledEvent.connect(self.onOrderCanceled)
		self.cancelOrderBtn.clicked.connect(self.cancelOrder)
		self.resetBtn.clicked.connect(self.resetFilter)
		self.searchBtn.clicked.connect(self.applyFilter)
		self.filteredBooksReceivedEvent.connect(self.fillFilteredBooks)
		self.nameFilterEdit.returnPressed.connect(self.applyFilter)
		self.genreFilterEdit.returnPressed.connect(self.applyFilter)
		
		self.booksUpdateBtn.hide()
		self.ordersUpdateBtn.hide()
		self.booksUpdateBtn.clicked.connect(lambda: self.updateTable("books"))
		self.ordersUpdateBtn.clicked.connect(lambda: self.updateTable("orders"))

		self.configureTables()
		self.booksTable.itemDoubleClicked.connect(self.showItemInfo)
		self.itemInfoReceivedEvent.connect(self.onItemInfoReceived)
		self.authorInfoForm = AuthorAddingForm(self, True)
		self.publisherInfoForm = PublisherAddingForm(self, True)

	def onItemInfoReceived(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return 
		getattr(self, self.requestedItemInfo + "InfoForm").showInfo(response.body)
		
	def showItemInfo(self, item: QTableWidgetItem):
		column = item.column()
		if column not in [3, 4]:
			return 
		name = item.text()
		if column == 3:
			request = RequestBuilder.Customer.getAuthorByName(name)
			self.requestedItemInfo = "author"
		else:
			request = RequestBuilder.Customer.getPublisherByName(name)
			self.requestedItemInfo = "publisher"

		self.processingForm.show()
		handler = lambda res: self.itemInfoReceivedEvent.emit(res)
		self.clientWorker.requestData(request, handler)

	def configureTables(self):
		for tableName in self.itemsMap:
			table: QTableWidget = getattr(self, tableName + "Table")
			for colIndex in range(table.columnCount()):
				table.horizontalHeader().setSectionResizeMode(colIndex, QHeaderView.ResizeToContents)
		
	def updateTable(self, tableName):
		table: QTableWidget = getattr(self, tableName + "Table")
		self.clearTable(table, tableName)
		if tableName == "books":
			self.applyFilter(True)
			self.booksUpdateBtn.hide()
			return 
		self.ordersTabLoaded = False
		self.onCurrentTabChanged(1)

	def onChangesReceived(self, response: Response):
		tables = set(response.body) & set(self.itemsMap)
		updateMessageTables = []
		for tableName in tables:
			updateBtn = getattr(self, tableName + "UpdateBtn")
			if updateBtn.isHidden():
				updateBtn.show()
				updateMessageTables.append(tableName)
		if len(updateMessageTables) == 0:
			return
		message = f"Some data has changed in: {', '.join(updateMessageTables)}"
		QMessageBox().information(self, "Changes update", message)

	def fillFilteredBooks(self, response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return
		self.clearTable(self.booksTable, "books")
		self.fillTable(self.booksTable, "books", response.body)
		
	def resetFilter(self):
		self.nameFilterEdit.clear()
		self.genreFilterEdit.clear()
		self.authorsList.setCurrentIndex(0)
		self.publishersList.setCurrentIndex(0)
		self.applyFilter(True)
		
	def applyFilter(self, reset=False):
		filters = [
			(self.nameFilterEdit.text(), "name"),
			(self.genreFilterEdit.text(), "genre"),
			(self.authorsList.currentText(), "author"),
			(self.publishersList.currentText(), "publisher")
		]
		filterParams = {}
		for filterValue, filterName in filters:
			if filterValue != "":
				filterParams[filterName] = filterValue
		if len(filterParams) == 0 and not reset:
			return 
		request = RequestBuilder.Customer.getBooks(filterParams)
		resHandler = lambda data: self.filteredBooksReceivedEvent.emit(data)
		self.clientWorker.requestData(request, resHandler)
		self.processingForm.show()

	def onOrderCanceled(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return
		self.ordersTable.removeRow(self.requestedItemInfo)
		self.itemsMap["orders"].pop(self.requestedItemInfo)
		if response.body not in self.itemsMap["books"]:
			return
		rowIndex = self.itemsMap["books"].index(response.body)
		bookCountCell = self.booksTable.item(rowIndex, 5)
		bookCountCell.setText(str(int(bookCountCell.text()) + 1))
		
	def cancelOrder(self):
		rowIndex = self.ordersTable.currentRow()
		if rowIndex < 0:
			return
		self.requestedItemInfo = rowIndex
		orderId = self.itemsMap["orders"][rowIndex]
		request = RequestBuilder.Customer.cancelOrder(orderId)
		responseHandler = lambda data: self.orderCanceledEvent.emit(data)
		self.clientWorker.requestData(request, responseHandler)
		self.processingForm.show()
		
	def onOrderMade(self, response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return
		bookCountCell = self.booksTable.item(self.requestedItemInfo, 5)
		bookCount = str(int(bookCountCell.text()) - 1)
		bookCountCell.setText(bookCount)
		self.clearTable(self.ordersTable, "orders")
		self.ordersTabLoaded = False
		
	def makeOrder(self):
		rowIndex = self.booksTable.currentRow()
		if rowIndex < 0:
			return
		bookCountCell = self.booksTable.item(rowIndex, 5)
		booksCount = int(bookCountCell.text())
		if booksCount == 0:
			self.showInvalidOperationMessage("There is no books left")
			return 
		self.requestedItemInfo = rowIndex
		
		bookId = self.itemsMap["books"][rowIndex]
		request = RequestBuilder.Customer.makeOrder(bookId)
		responseHandler = lambda data: self.orderMadeEvent.emit(data)
		self.clientWorker.requestData(request, responseHandler)
		self.processingForm.show()
		
	def init(self):
		self.show()
		self.processingForm.show()
		Thread(target=self.requestInitData).start()
		
	def requestInitData(self):
		handleInitialData = lambda data: self.initialDataReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getBooksPageData()
		self.clientWorker.requestData(request, handleInitialData)
		
	def initBooksPage(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return
		self.authorsList.addItems(response.body["authorsNames"])
		self.publishersList.addItems(response.body["publishersNames"])
		self.fillTable(self.booksTable, "books", response.body["books"])
				
	def onCurrentTabChanged(self, index):
		if index == 0 or self.ordersTabLoaded:
			return
		self.ordersTabLoaded = True
		self.ordersUpdateBtn.hide()
		handleResponse = lambda data: self.ordersReceivedEvent.emit(data)
		request = RequestBuilder.Customer.getOrders()
		self.clientWorker.requestData(request, handleResponse)
		
	def initOrdersPage(self, response: Response):
		if not response.succeed:
			self.showErrorMessage("User orders fetch error", response.errorMessage)
			return
		self.fillTable(self.ordersTable, "orders", response.body)
		
	def clearTable(self, tableWidget: QTableWidget, tableName):
		tableWidget.clearContents()
		tableWidget.setRowCount(0)
		self.itemsMap[tableName].clear()
		
	def fillTable(self, tableWidget: QTableWidget, tableName, items):
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
		
	def closeEvent(self, event: QCloseEvent):		
		self.clientWorker.closeConnection()
		event.accept()

	def showErrorMessage(self, title, message):
		QMessageBox().critical(self, title, message)
		self.close()
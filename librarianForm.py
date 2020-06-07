from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView

from clientWorker import ClientWorker
from models import Response
from processingForm import ProcessingForm
from requestBuilder import RequestBuilder
from ui.convertedUi.librarianForm import Ui_librarianForm

class LibrarianForm(Ui_librarianForm, QWidget):
	booksInitialDataReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()
	filteredBooksReceivedEvent = pyqtSignal(object)
	changesReceivedEvent = pyqtSignal(object)
	itemDeletedEvent = pyqtSignal(object)
	pageInitialDataReceivedEvent = pyqtSignal(object)
	
	def __init__(self, clientWorker: ClientWorker):
		super().__init__(None, Qt.WindowCloseButtonHint)
		self.setupUi(self)
		self.clientWorker = clientWorker
		self.processingForm = ProcessingForm(self)
		self.booksInitialDataReceivedEvent.connect(self.initBooksPage)
		self.serverConnectionLostEvent.connect(self.onServerConnectionLost)
		clientWorker.onServerDisconnected = lambda: self.serverConnectionLostEvent.emit()
		self.itemsMap = {
			"orders":[],
			"books":[],
			"publishers": [],
			"authors": []
		}
		self.loadedPages = {i:False for i in self.itemsMap if i != "books"}
		self.configureTables()
		self.tabWidget.currentChanged.connect(self.onCurrentTabChanged)

		self.resetBtn.clicked.connect(self.resetFilter)
		self.searchBtn.clicked.connect(self.applyFilter)
		self.nameFilterEdit.returnPressed.connect(self.applyFilter)
		self.genreFilterEdit.returnPressed.connect(self.applyFilter)
		self.filteredBooksReceivedEvent.connect(self.fillFilteredBooks)
		
		self.booksUpdateBtn.hide()
		self.ordersUpdateBtn.hide()
		self.booksUpdateBtn.clicked.connect(lambda: self.updateTable("books"))
		self.ordersUpdateBtn.clicked.connect(lambda: self.updateTable("orders"))
		self.changesReceivedEvent.connect(self.onChangesReceived)
		clientWorker.onChangesReceived = lambda data: self.changesReceivedEvent.emit(data)

		self.delBookBtn.clicked.connect(lambda: self.deleteItem("books"))
		self.deletingItemInfo = None
		self.itemDeletedEvent.connect(self.onItemDeleted)
		
		self.pageInitialDataReceivedEvent.connect(self.initPage)
		self.initializingTableName = None
		
	def initPage(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return 
		table = getattr(self, self.initializingTableName + "Table")
		self.fillTable(table, self.initializingTableName, response.body)
		
	def onCurrentTabChanged(self, index):
		if index == 0:
			return
		tabName = self.tabWidget.tabText(index).lower()
		if self.loadedPages[tabName]:
			return
		self.processingForm.showRequestProcessing()
		self.initializingTableName = tabName
		self.loadedPages[tabName] = True
		request = getattr(RequestBuilder.Librarian, tabName + "GetAll")()
		handleResponse = lambda res: self.pageInitialDataReceivedEvent.emit(res)
		self.clientWorker.requestData(request, handleResponse)

	def onItemDeleted(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return 
		table: QTableWidget
		table, rowIndex = self.deletingItemInfo
		table.removeRow(rowIndex)
		if response.body is not None:
			print(f"Update {', '.join(response.body)}")
		
	def deleteItem(self, tableName):
		self.processingForm.showRequestProcessing()
		table: QTableWidget = getattr(self, tableName + "Table")
		rowIndex = table.currentRow()
		self.deletingItemInfo = (table, rowIndex)
		itemId = self.itemsMap[tableName][rowIndex]
		request = getattr(RequestBuilder.Librarian, tableName + "Delete")(itemId)
		handleResponse = lambda data: self.itemDeletedEvent.emit(data)
		self.clientWorker.requestData(request, handleResponse)

	def updateTable(self, tableName):
		table: QTableWidget = getattr(self, tableName + "Table")
		self.clearTable(table, tableName)
		if tableName == "books":
			self.applyFilter(True)
			self.booksUpdateBtn.hide()
			return
		self.loadedPages[tableName] = False
		self.onCurrentTabChanged(self.tabWidget.currentIndex())

	def onChangesReceived(self, response: Response):
		tables = set(response.body) & set(self.itemsMap)
		message = f"Some data has changed in: {', '.join(tables)}"
		QMessageBox().information(self, "Changes update", message)
		for tableName in tables:
			getattr(self, tableName + "UpdateBtn").show()

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
		request = RequestBuilder.Librarian.getBooks(filterParams)
		resHandler = lambda data: self.filteredBooksReceivedEvent.emit(data)
		self.clientWorker.requestData(request, resHandler)
		self.processingForm.showRequestProcessing()

	def fillFilteredBooks(self, response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return
		self.clearTable(self.booksTable, "books")
		self.fillTable(self.booksTable, "books", response.body)

	def configureTables(self):
		for tableName in self.itemsMap:
			table: QTableWidget = getattr(self, tableName + "Table")
			for colIndex in range(table.columnCount()):
				table.horizontalHeader().setSectionResizeMode(colIndex, QHeaderView.ResizeToContents)

	def init(self):
		self.show()
		self.processingForm.showRequestProcessing()
		Thread(target=self.requestInitData).start()

	def requestInitData(self):
		handleInitialData = lambda data: self.booksInitialDataReceivedEvent.emit(data)
		request = RequestBuilder.Librarian.getBooksPageData()
		self.clientWorker.requestData(request, handleInitialData)

	def initBooksPage(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.message)
			return
		self.authorsList.addItems(response.body["authorsNames"])
		self.publishersList.addItems(response.body["publishersNames"])
		self.fillTable(self.booksTable, "books", response.body["books"])

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

	def showInvalidOperationMessage(self, message):
		QMessageBox().warning(self, "Invalid operation", message)

	def onServerConnectionLost(self):
		QMessageBox.critical(self, "Error", "Server connection lost")
		self.close()

	def closeEvent(self, event: QCloseEvent):
		self.clientWorker.closeConnection()
		event.accept()

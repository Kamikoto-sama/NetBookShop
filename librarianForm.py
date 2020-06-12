from threading import Thread
from typing import List, Dict

from PyQt5.QtCore import pyqtSignal, Qt, QMimeData
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QPushButton, QComboBox

from authorAddingForm import AuthorAddingForm
from bookAddingForm import BookAddingForm
from clientWorker import ClientWorker
from models import Response, EntityChanges
from processingForm import ProcessingForm
from publisherAddingForm import PublisherAddingForm
from requestBuilder import RequestBuilder
from ui.convertedUi.librarianForm import Ui_librarianForm

class LibrarianForm(Ui_librarianForm, QWidget):
	booksInitialDataReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()
	filteredBooksReceivedEvent = pyqtSignal(object)
	changesReceivedEvent = pyqtSignal(object)
	itemDeletedEvent = pyqtSignal(object)
	pageInitialDataReceivedEvent = pyqtSignal(object)
	changesSavedEvent = pyqtSignal(object)
	itemAddedEvent = pyqtSignal(object)
	
	def __init__(self, clientWorker: ClientWorker):
		super().__init__(None, Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
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
		self.filteredBooksReceivedEvent.connect(self.onFilteredBooksReceived)
		
		self.booksUpdateBtn.hide()
		self.ordersUpdateBtn.hide()
		self.booksUpdateBtn.clicked.connect(lambda: self.updateTable("books"))
		self.ordersUpdateBtn.clicked.connect(lambda: self.updateTable("orders"))
		self.changesReceivedEvent.connect(self.onChangesReceived)
		clientWorker.onChangesReceived = lambda data: self.changesReceivedEvent.emit(data)

		self.delBookBtn.clicked.connect(lambda: self.deleteItem("books"))
		self.delAuthorBtn.clicked.connect(lambda: self.deleteItem("authors"))
		self.delPublisherBtn.clicked.connect(lambda: self.deleteItem("publishers"))
		self.delOrderBtn.clicked.connect(lambda: self.deleteItem("orders"))
		self.deletingItemInfo = None
		self.tabsMap = ["books", "authors", "publishers", "orders"]
		self.itemDeletedEvent.connect(self.onItemDeleted)
		
		self.pageInitialDataReceivedEvent.connect(self.initPage)
		self.processingTableName = None
		
		self.selectedCell = None
		self.booksTable.itemChanged.connect(lambda item: self.onCellChanged(item, "books"))
		self.authorsTable.itemChanged.connect(lambda item: self.onCellChanged(item, "authors"))
		self.publishersTable.itemChanged.connect(lambda item: self.onCellChanged(item, "publishers"))
		self.booksTable.itemDoubleClicked.connect(lambda item: setattr(self, "selectedCell", item))
		self.authorsTable.itemDoubleClicked.connect(lambda item: setattr(self, "selectedCell", item))
		self.publishersTable.itemDoubleClicked.connect(lambda item: setattr(self, "selectedCell", item))
		self.entitiesFields: Dict[list] = {}
		self.booksSaveChangesBtn.clicked.connect(lambda: self.saveChanges("books"))
		self.authorsSaveChangesBtn.clicked.connect(lambda: self.saveChanges("authors"))
		self.publishersSaveChangesBtn.clicked.connect(lambda: self.saveChanges("publishers"))
		self.changes: Dict[EntityChanges] = {table:EntityChanges() for table in self.itemsMap if table != "orders"}
		self.changesSavedEvent.connect(self.onChangesSaved)
		
		self.bookAddBtn.clicked.connect(lambda: self.addItem("books"))
		self.authorAddBtn.clicked.connect(lambda: self.addItem("authors"))
		self.publisherAddBtn.clicked.connect(lambda: self.addItem("publishers"))
		self.booksAddingForm = BookAddingForm(self)
		self.authorsAddingForm = AuthorAddingForm(self)
		self.publishersAddingForm = PublisherAddingForm(self)
		self.itemAddedEvent.connect(self.onItemAdded)
		
		self.searchAuthorBtn.clicked.connect(lambda: self.applyNameFilter("authors"))
		self.searchPublisherBtn.clicked.connect(lambda: self.applyNameFilter("publishers"))
		self.resetAuthorsBtn.clicked.connect(lambda: self.resetNameFilter("authors"))
		self.resetPublishersBtn.clicked.connect(lambda: self.resetNameFilter("publishers"))
		
	def resetNameFilter(self, tableName):
		self.updateTable(tableName)
		self.changes[tableName].clearChanges()
		getattr(self, tableName + "SaveChangesBtn").setDisabled(True)
		
	def applyNameFilter(self, tableName):
		nameList: QComboBox = getattr(self, tableName + "List2")
		name = nameList.currentText()
		if name == "":
			return
		table: QTableWidget = getattr(self, tableName + "Table")
		items = table.findItems(name, Qt.MatchContains)
		if len(items) == 0:
			return 
		rowIndex = items[0].row()
		entityId = self.itemsMap[tableName][rowIndex]
		entity = {"id":entityId}
		for i in range(table.columnCount()):
			entity[i] = table.item(rowIndex, i).text()
		table.clearContents()
		self.itemsMap[tableName].clear()
		self.fillTable(table, tableName, [entity])
		
	def onItemAdded(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return
		self.updateTable(self.processingTableName)
		
	def addItem(self, tableName):
		addingForm = getattr(self, tableName + "AddingForm")
		if tableName == "books":
			authorsNames = [self.authorsList.itemText(i) for i in range(self.authorsList.count())]
			publishersNames = [self.publishersList.itemText(i) for i in range(self.publishersList.count())]
			addingForm.fillLists(authorsNames, publishersNames)
		addingForm.show()

	def onChangesSaved(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return
		getattr(self, self.processingTableName + "SaveChangesBtn").setDisabled(True)
		self.changes[self.processingTableName].clearChanges()
		for tableName in response.body:
			self.updateTable(tableName)

	def saveChanges(self, tableName):
		self.processingForm.show()
		self.processingTableName = tableName
		request = getattr(RequestBuilder.Librarian, tableName + "Update")(self.changes[tableName])
		resHandler = lambda res: self.changesSavedEvent.emit(res)
		self.clientWorker.requestData(request, resHandler)
		
	def fillEntityFields(self, entities: List[dict], entityName):
		if entityName in self.entitiesFields or entities is None or len(entities) == 0:
			return 
		entity: dict = entities[0]
		self.entitiesFields[entityName] = [field for field in entity.keys() if field != "id"]
		
	def onCellChanged(self, item: QTableWidgetItem, tableName):
		if self.selectedCell != item:
			self.selectedCell = None
			return
		value = item.text()
		self.selectedCell = None
		if value == "":
			self.showInvalidOperationMessage("Field can't be empty. Changes unsaved")
			return 
		getattr(self, tableName + "SaveChangesBtn").setEnabled(True)
		entityChanges: EntityChanges = self.changes[tableName]
		fieldName = self.entitiesFields[tableName][item.column()]
		itemId = self.itemsMap[tableName][item.row()]
		entityChanges.saveChanges(itemId, fieldName, value)
		
	def initPage(self, response: Response):
		self.processingForm.hide()
		getattr(self, self.processingTableName + "UpdateBtn").hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return 
		table = getattr(self, self.processingTableName + "Table")
		self.fillTable(table, self.processingTableName, response.body)
		self.fillEntityFields(response.body, self.processingTableName)
		if self.processingTableName != "orders":
			self.updateList(self.processingTableName, [i["name"] for i in response.body])

	def updateList(self, tableName, items):
		items = ["", *items]
		listWidget1: QComboBox = getattr(self, tableName + "List")
		listWidget2: QComboBox = getattr(self, tableName + "List2")
		listWidget1.clear()
		listWidget2.clear()
		listWidget1.addItems(items)
		listWidget2.addItems(items)
		
	def onCurrentTabChanged(self, index):
		if index == 0:
			return
		tabName = self.tabWidget.tabText(index).lower()
		if self.loadedPages[tabName]:
			return
		self.processingForm.show()
		self.processingTableName = tabName
		self.loadedPages[tabName] = True
		request = getattr(RequestBuilder.Librarian, tabName + "GetAll")()
		handleResponse = lambda res: self.pageInitialDataReceivedEvent.emit(res)
		self.clientWorker.requestData(request, handleResponse)

	def onItemDeleted(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return
		for tableName in response.body:
			self.updateTable(tableName)
		
	def deleteItem(self, tableName):
		table: QTableWidget = getattr(self, tableName + "Table")
		rowIndex = table.currentRow()
		if rowIndex < 0:
			return
		self.processingForm.show()
		itemId = self.itemsMap[tableName][rowIndex]
		self.deletingItemInfo = (tableName, rowIndex, itemId)
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
		tabIndex = self.tabsMap.index(tableName)
		self.onCurrentTabChanged(tabIndex)
		getattr(self, tableName + "UpdateBtn").hide()

	def onChangesReceived(self, response: Response):
		tables = set(response.body) & set(self.itemsMap)
		updateMessageTables = []
		for tableName in tables:
			updateBtn: QPushButton = getattr(self, tableName + "UpdateBtn")
			if updateBtn.isHidden():
				updateBtn.show()
				updateMessageTables.append(tableName)
		if len(updateMessageTables) == 0:
			return
		message = f"Some data has changed in: {', '.join(updateMessageTables)}"
		QMessageBox().information(self, "Changes update", message)

	def resetFilter(self):
		self.nameFilterEdit.clear()
		self.genreFilterEdit.clear()
		self.authorsList.setCurrentIndex(0)
		self.publishersList.setCurrentIndex(0)
		self.changes["books"].clearChanges()
		self.booksSaveChangesBtn.setDisabled(True)
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
		self.processingForm.show()

	def onFilteredBooksReceived(self, response):
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
		self.processingForm.show()
		Thread(target=self.requestInitData).start()

	def requestInitData(self):
		handleInitialData = lambda data: self.booksInitialDataReceivedEvent.emit(data)
		request = RequestBuilder.Librarian.getBooksPageData()
		self.clientWorker.requestData(request, handleInitialData)

	def initBooksPage(self, response: Response):
		self.processingForm.hide()
		if not response.succeed:
			self.showInvalidOperationMessage(response.errorMessage)
			return
		self.authorsList.addItems(response.body["authorsNames"])
		self.publishersList.addItems(response.body["publishersNames"])
		self.fillTable(self.booksTable, "books", response.body["books"])
		self.fillEntityFields(response.body["books"], "books")

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

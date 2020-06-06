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
	initialDataReceivedEvent = pyqtSignal(object)
	serverConnectionLostEvent = pyqtSignal()

	def __init__(self, clientWorker: ClientWorker):
		super().__init__(None, Qt.WindowCloseButtonHint)
		self.setupUi(self)
		self.clientWorker = clientWorker
		self.processingForm = ProcessingForm(self)
		self.initialDataReceivedEvent.connect(self.initBooksPage)
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

	def onCurrentTabChanged(self, index):
		if index == 0:
			return 
		tabName = self.tabWidget.tabText(index).lower()
		if self.loadedPages[tabName]:
			return
		self.loadedPages[tabName] = True
		print(tabName, self.loadedPages)
		
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
		handleInitialData = lambda data: self.initialDataReceivedEvent.emit(data)
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

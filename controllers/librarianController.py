from controllers.baseController import BaseController
from models import Role, ChangesEvent, EntityChanges
from repositories.authorsRepository import AuthorsRepository
from repositories.booksRepository import BooksRepository
from repositories.ordersRepository import OrdersRepository
from repositories.publishersRepository import PublishersRepository


class LibrarianController(BaseController):
	allowedRole = Role.LIBRARIAN

	def addPublisher(self, publisherData: dict):
		PublishersRepository.addPublisher(publisherData)
		changesEvent = ChangesEvent(["publishers"], [Role.CUSTOMER, Role.LIBRARIAN], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok()
	
	def addAuthor(self, authorData: dict):
		AuthorsRepository.addAuthor(authorData)
		changesEvent = ChangesEvent(["authors"], [Role.CUSTOMER, Role.LIBRARIAN], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok()
	
	def addBook(self, bookData: dict):
		result = self.replaceNamesToIds(bookData)
		if result is not None:
			return result
		book = BooksRepository.addBook(bookData)
		changesEvent = ChangesEvent(["books"], [Role.CUSTOMER, Role.LIBRARIAN], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(book)

	def updatePublishers(self, changesData: str):
		changesContainer = EntityChanges.fromJson(changesData)
		changedTables = {"publishers"}
		for publisherId, changes in changesContainer.changes.items():
			PublishersRepository.updatePublisherById(publisherId, changes)
			books = BooksRepository.getBooksByPublisherId(publisherId)
			if len(books) > 0 and "name" in changes:
				changedTables.add("books")

		changedTables = list(changedTables)
		changesEvent = ChangesEvent(changedTables, [Role.CUSTOMER, Role.LIBRARIAN], exceptClientId=self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(changedTables)

	def updateAuthors(self, changesData: str):
		changesContainer = EntityChanges.fromJson(changesData)
		changedTables = {"authors"}
		for authorId, changes in changesContainer.changes.items():
			AuthorsRepository.updateAuthorById(authorId, changes)
			books = BooksRepository.getBooksByAuthorId(authorId)
			if len(books) > 0 and "name" in changes:
				changedTables.add("books")

		changedTables = list(changedTables)
		changesEvent = ChangesEvent(changedTables, [Role.CUSTOMER, Role.LIBRARIAN], exceptClientId=self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(changedTables)

	def updateBooks(self, changesData: str):
		changesContainer = EntityChanges.fromJson(changesData)
		changedTables = {"books"}
		for bookId, changes in changesContainer.changes.items():
			orders = OrdersRepository.getOrdersByBookId(bookId)
			if len(orders) > 0 and "name" in changes:
				changedTables.add("orders")
			result = self.replaceNamesToIds(changes)
			if result is not None:
				return result
			BooksRepository.updateBookById(bookId, changes)

		changedTables = list(changedTables)
		changesEvent = ChangesEvent(changedTables, [Role.CUSTOMER, Role.LIBRARIAN], exceptClientId=self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(changedTables)
	
	def getAllPublishers(self):
		publishers = PublishersRepository.getAllPublishers()
		return self.ok(publishers)
	
	def getAllOrders(self):
		orders = OrdersRepository.getAllOrders()
		return self.ok(orders)
	
	def deletePublisher(self, publisherId):
		tables = {"publishers"}
		books = BooksRepository.getBooksByPublisherId(publisherId)
		self.cascadeDelete(books, tables)
		PublishersRepository.deletePublisherById(publisherId)
		tables = list(tables)
		changesEvent = ChangesEvent(tables, [Role.LIBRARIAN, Role.CUSTOMER], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(tables)
	
	def deleteAuthor(self, authorId):
		tables = {"authors"}
		books = BooksRepository.getBooksByAuthorId(authorId)
		self.cascadeDelete(books, tables)
		AuthorsRepository.deleteAuthorById(authorId)
		table = list(tables)
		changesEvent = ChangesEvent(table, [Role.LIBRARIAN, Role.CUSTOMER], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(table)
	
	@staticmethod
	def cascadeDelete(books, tables: set):
		for book in books:
			tables.add("books")
			orders = OrdersRepository.getOrdersByBookId(book["id"])
			for order in orders:
				tables.add("orders")
				OrdersRepository.deleteOrderById(order["id"])
			BooksRepository.deleteBookById(book["id"])
	
	def deleteOrder(self, orderId):
		book = OrdersRepository.getOrderById(orderId).book
		book.count += 1
		book.save()
		OrdersRepository.deleteOrderById(orderId)
		tables = ["orders", "books"]
		changesEvent = ChangesEvent(tables, [Role.LIBRARIAN, Role.CUSTOMER], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(tables)
	
	def deleteBook(self, bookId):
		tables = ["books"]
		orders = OrdersRepository.getOrdersByBookId(bookId)
		BooksRepository.deleteBookById(bookId)
		for order in orders:
			OrdersRepository.deleteOrderById(order["id"])
			tables.append("orders")
		changesEvent = ChangesEvent(tables, [Role.LIBRARIAN, Role.CUSTOMER], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		return self.ok(tables)

	def getBooks(self, filterParams: dict):
		result = self.replaceNamesToIds(filterParams)
		if result is not None:
			return self.ok(body=[])
		books = BooksRepository.getBooks(filterParams)
		return self.ok(body=books)
	
	def replaceNamesToIds(self, items: dict):
		if "author" in items:
			author = AuthorsRepository.getAuthorByName(items["author"])
			if author is None:
				return self.badRequest(f"Unknown author {items['author']}")
			items["author"] = author["id"]
		if "publisher" in items:
			publisher = PublishersRepository.getPublisherByName(items["publisher"])
			if publisher is None:
				return self.badRequest(f"Unknown publisher {items['publisher']}")
			items["publisher"] = publisher["id"]
	
	def getAllAuthors(self):
		authors = AuthorsRepository.getAllAuthors()
		return self.ok(authors)
	
	def getBooksPageData(self):
		books = BooksRepository.getBooks({})
		authors = AuthorsRepository.getAllAuthors()
		authorsNames = [author["name"] for author in authors]
		publishers = PublishersRepository.getAllPublishers()
		publishersNames = [author["name"] for author in publishers]
		data = {
			"books": books,
			"authorsNames": authorsNames,
			"publishersNames": publishersNames
		}
		return self.ok(data)
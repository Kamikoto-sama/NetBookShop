from controllers.baseController import BaseController
from models import Role, ChangesEvent, EntityChanges
from repositories.authorsRepository import AuthorsRepository
from repositories.booksRepository import BooksRepository
from repositories.ordersRepository import OrdersRepository
from repositories.publishersRepository import PublishersRepository


class LibrarianController(BaseController):
	allowedRole = Role.LIBRARIAN

	def updateBooks(self, changesData: str):
		changesContainer = EntityChanges.fromJson(changesData)
		changedTables = ["books"]
		for bookId, changes in changesContainer.changes.items():
			BooksRepository.updateBookById(bookId, changes)
			order = OrdersRepository.getOrderByBookId(bookId)
			if order is not None and "name" in changes:
				changedTables.append("orders")
		changesEvent = ChangesEvent(changedTables, [Role.CUSTOMER, Role.LIBRARIAN], exceptClientId=self.userInfo.id)
		self.callChangesEvent(changesEvent)
		update = set(changedTables) - {"books"}
		return self.ok(update)
	
	def getAllPublishers(self):
		publishers = PublishersRepository.getAllPublishers()
		return self.ok(publishers)
	
	def getAllOrders(self):
		orders = OrdersRepository.getAllOrders()
		return self.ok(orders)

	def deleteBook(self, bookId):
		tables = ["books"]
		order = OrdersRepository.getOrderByBookId(bookId)
		BooksRepository.deleteBookById(bookId)
		if order is not None:
			tables.append("orders")
		changesEvent = ChangesEvent(tables, [Role.LIBRARIAN, Role.CUSTOMER], self.userInfo.id)
		self.callChangesEvent(changesEvent)
		body = ["orders"] if order is not None else []
		return self.ok(body)

	def getBooks(self, filterParams: dict):
		if "author" in filterParams:
			authors = AuthorsRepository.getAuthorsByName(filterParams["author"])
			if len(authors) == 0:
				return self.badRequest(f"Unknown author {filterParams['author']}")
			filterParams["author"] = authors[0]["id"]
		if "publisher" in filterParams:
			publishers = PublishersRepository.getPublishersByName(filterParams["publisher"])
			if len(publishers) == 0:
				return self.badRequest(f"Unknown publisher {filterParams['publisher']}")
			filterParams["publisher"] = publishers[0]["id"]
		books = BooksRepository.getBooks(filterParams)
		return self.ok(body=books)
	
	def getAllAuthors(self):
		authors = AuthorsRepository.getAllAuthors()
		return self.ok(authors)
	
	def getAuthorByName(self, authorName):
		author = AuthorsRepository.getAuthorsByName(authorName)
		if author is None:
			return self.badRequest("Unknown author")
		self.ok(author)

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
from controllers.baseController import BaseController
from models import Role, ChangesEvent
from repositories.authorsRepository import AuthorsRepository
from repositories.booksRepository import BooksRepository
from repositories.ordersRepository import OrdersRepository
from repositories.publishersRepository import PublishersRepository


class CustomerController(BaseController):
	allowedRole = Role.CUSTOMER

	def getPublisherByName(self, publisherName):
		publisher = PublishersRepository.getPublisherByName(publisherName)
		if publisher is None:
			return self.badRequest("Unknown publisher")
		return self.ok(publisher)
	
	def getAuthorByName(self, authorName):
		author = AuthorsRepository.getAuthorByName(authorName)
		if author is None:
			return self.badRequest("Unknown author")
		return self.ok(author)

	def getOrders(self):
		orders = OrdersRepository.getUserOrders(self.userInfo.id)
		return self.ok(body=orders)
	
	def makeOrder(self, bookId):
		book = BooksRepository.getBookById(bookId)
		if book is None:
			return self.badRequest("No such book")
		if book["count"] > 0:
			BooksRepository.updateBookById(bookId, {"count": book["count"] - 1})
		else:
			return self.badRequest("There is no book left")
			
		OrdersRepository.addOrder(self.userInfo.id, bookId)
		changesEvent = ChangesEvent(["orders", "books"], [Role.LIBRARIAN])
		self.callChangesEvent(changesEvent)
		return self.ok()
	
	def cancelOrder(self, orderId):
		order = OrdersRepository.getOrderById(orderId)
		order.book.count += 1
		order.book.save()
		OrdersRepository.deleteOrderById(orderId)
		changesEvent = ChangesEvent(["orders", "books"], [Role.LIBRARIAN])
		self.callChangesEvent(changesEvent)
		return self.ok(body=order.book.id)
	
	def getBooks(self, filterParams: dict):
		if "author" in filterParams:
			author = AuthorsRepository.getAuthorByName(filterParams["author"])
			if author is None:
				return self.badRequest(f"Unknown author {filterParams['author']}")
			filterParams["author"] = author["id"]
		if "publisher" in filterParams:
			publisher = PublishersRepository.getPublisherByName(filterParams["publisher"])
			if publisher is None:
				return self.badRequest(f"Unknown publisher {filterParams['publisher']}")
			filterParams["publisher"] = publisher["id"]
		books = BooksRepository.getBooks(filterParams)
		return self.ok(body=books)
	
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
		return self.ok(body=data)
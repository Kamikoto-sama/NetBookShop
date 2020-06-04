from controllers.baseController import BaseController
from models import Role, ChangesUpdateEvent
from repositories.authorsRepository import AuthorsRepository
from repositories.booksRepository import BooksRepository
from repositories.ordersRepository import OrdersRepository
from repositories.publishersRepository import PublishersRepository


class CustomerController(BaseController):
	allowedRole = Role.CUSTOMER

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
		changes = {"orders": OrdersRepository.getAllOrders()}
		changesEvent = ChangesUpdateEvent(["orders"], changes, [Role.LIBRARIAN])
		self.changesUpdateEvent(changesEvent)
		return self.ok()
	
	def cancelOrder(self, orderId):
		order = OrdersRepository.getOrderById(orderId)
		order.book.count += 1
		order.book.save()
		OrdersRepository.deleteOrderById(orderId)
		return self.ok()
	
	def getBooks(self, filterParams: dict):
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
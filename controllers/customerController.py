from controllers.baseController import BaseController
from models import Role
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
		OrdersRepository.addOrder(self.userInfo.id, bookId)
		return self.ok()
	
	def cancelOrder(self, orderId):
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
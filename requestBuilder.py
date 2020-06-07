from controllersMap import Controllers
from models import Request

class RequestBuilder:
	class Auth:
		@staticmethod
		def register(loginData: dict):
			return Request(Controllers.Auth, "register", loginData)

		@staticmethod
		def login(loginData: dict):
			return Request(Controllers.Auth, "login", loginData)
		
	class Librarian:
		@staticmethod
		def getBooksPageData():
			return Request(Controllers.Librarian, "getBooksPageData")
		
		@staticmethod
		def getAuthorByName(authorName):
			return Request(Controllers.Librarian, "getAuthorByName", authorName)
		
		@staticmethod
		def getBooks(filterParams: dict):
			return Request(Controllers.Librarian, "getBooks", filterParams)
		
		@staticmethod
		def booksDelete(bookId):
			return Request(Controllers.Librarian, "deleteBook", bookId)

		@staticmethod
		def authorsGetAll():
			return Request(Controllers.Librarian, "getAllAuthors")
		
		@staticmethod
		def publishersGetAll():
			return Request(Controllers.Librarian, "getAllPublishers")
		
		@staticmethod
		def ordersGetAll():
			return Request(Controllers.Librarian, "getAllOrders")
		
	class Customer:
		@staticmethod
		def getOrders():
			return Request(Controllers.Customer, "getOrders")

		@staticmethod
		def makeOrder(bookId):
			return Request(Controllers.Customer, "makeOrder", bookId)

		@staticmethod
		def cancelOrder(orderId):
			return Request(Controllers.Customer, "cancelOrder", orderId)

		@staticmethod
		def getBooks(filterParams: dict):
			return Request(Controllers.Customer, "getBooks", filterParams)

		@staticmethod
		def getBooksPageData():
			return Request(Controllers.Customer, "getBooksPageData")
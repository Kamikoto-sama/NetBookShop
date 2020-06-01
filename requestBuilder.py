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
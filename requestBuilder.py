from controllersMap import Controllers
from models import Request, EntityChanges


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
		
		@staticmethod
		def booksUpdate(changes: EntityChanges):
			return Request(Controllers.Librarian, "updateBooks", changes.toJson())
		
		@staticmethod
		def authorsUpdate(changes: EntityChanges):
			return Request(Controllers.Librarian, "updateAuthors", changes.toJson())

		@staticmethod
		def publishersUpdate(changes: EntityChanges):
			return Request(Controllers.Librarian, "updatePublishers", changes.toJson())
		
		@staticmethod
		def addBook(bookData: dict):
			return Request(Controllers.Librarian, "addBook", bookData)
		
		@staticmethod
		def addAuthor(authorData: dict):
			return Request(Controllers.Librarian, "addAuthor", authorData)

		@staticmethod
		def addPublisher(publisherData: dict):
			return Request(Controllers.Librarian, "addPublisher", publisherData)
		
		@staticmethod
		def authorsDelete(authorId):
			return Request(Controllers.Librarian, "deleteAuthor", authorId)
		
		@staticmethod
		def ordersDelete(orderId):
			return Request(Controllers.Librarian, "deleteOrder", orderId)
		
		@staticmethod
		def publishersDelete(publisherId):
			return Request(Controllers.Librarian, "deletePublisher", publisherId)
		
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

		@staticmethod
		def getAuthorByName(authorName):
			return Request(Controllers.Customer, "getAuthorByName", authorName)

		@staticmethod
		def getAuthorsAndPublishers(tables: list):
			return Request(Controllers.Customer, "getAuthorsAndPublishers", tables)
		
		@staticmethod
		def getPublisherByName(publisherName):
			return Request(Controllers.Customer, "getPublisherByName", publisherName)
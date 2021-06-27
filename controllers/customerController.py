from controllers.baseController import BaseController
from models import Role, ChangesEvent
from repositories.authorsRepository import AuthorsRepository
from repositories.booksRepository import BooksRepository
from repositories.ordersRepository import OrdersRepository
from repositories.publishersRepository import PublishersRepository

class CustomerController(BaseController):
    allowedRole = Role.CUSTOMER

    def getAuthorsAndPublishers(self, tables: list):
        if len(set(tables) & {"authors", "publishers"}) == 0:
            return self.badRequest(f"Invalid {tables = }")
        responseData = {}
        if "authors" in tables:
            authors = AuthorsRepository.getAllAuthors()
            authors = [a["name"] for a in authors]
            responseData["authors"] = authors
        if "publishers" in tables:
            publishers = PublishersRepository.getAllPublishers()
            publishers = [p["name"] for p in publishers]
            responseData["publishers"] = publishers

        return self.ok(responseData)

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

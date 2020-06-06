from controllers.baseController import BaseController
from models import Role
from repositories.authorsRepository import AuthorsRepository
from repositories.booksRepository import BooksRepository
from repositories.publishersRepository import PublishersRepository


class LibrarianController(BaseController):
	allowedRole = Role.LIBRARIAN
	
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
from dataBaseContext import Author


class AuthorsRepository:
	@staticmethod
	def addAuthor(authorData: dict):
		authorId = Author.create(**authorData)
		author = list(Author.select().where(Author.id == authorId))[0]
		return author

	@staticmethod
	def getAuthorByName(authorName) -> dict:
		author = Author.select().where(Author.name == authorName).dicts().first()
		return author
	
	@staticmethod
	def getAllAuthors():
		return list(Author.select().dicts())

	@staticmethod
	def updateAuthorById(authorId, updatedValues: dict):
		Author.update(**updatedValues).where(Author.id == authorId).execute()

	@staticmethod
	def deleteAuthorById(authorId):
		Author.delete_by_id(authorId)
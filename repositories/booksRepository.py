from typing import List

from dataBaseContext import Book, Author, Publisher

class BooksRepository:

    @staticmethod
    def getBooks(filterParams: dict) -> List[dict]:
        query = Book.select(Book.id, Book.name, Book.genre, Book.pageCount,
                            Author.name.alias("author"), Publisher.name.alias("publisher"),
                            Book.count, Book.price).join(Author, on=(Book.author == Author.id)) \
            .join(Publisher, on=(Book.publisher == Publisher.id)).dicts()
        if len(filterParams) == 0:
            return list(query)
        books = query.filter(**filterParams)
        return list(books)

    @staticmethod
    def getBooksByAuthorId(authorId):
        book = Book.select().where(Book.author == Author.get(id=authorId)).dicts()
        return book

    @staticmethod
    def getBooksByPublisherId(publisherId):
        book = Book.select().where(Book.publisher == Publisher.get(id=publisherId)).dicts()
        return book

    @staticmethod
    def getBookById(bookId):
        book = Book.select(Book.id, Book.name, Book.genre, Book.pageCount,
                           Author.name.alias("author"), Publisher.name.alias("publisher"),
                           Book.count, Book.price).join(Author, on=(Book.author == Author.id)) \
            .join(Publisher, on=(Book.publisher == Publisher.id)) \
            .where(Book.id == bookId).dicts().first()
        return book

    @staticmethod
    def addBook(bookData: dict):
        bookId = Book.create(**bookData).id
        book = Book.select().where(Book.id == bookId).dicts().first()
        return book

    @staticmethod
    def updateBookById(bookId, changes: dict):
        Book.update(**changes).where(Book.id == bookId).execute()

    @staticmethod
    def deleteBookById(bookId):
        Book.delete_by_id(bookId)

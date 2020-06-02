from datetime import date

from peewee import *

from models import Role

db = SqliteDatabase("data.db")

class BaseModel(Model):
	class Meta:
		database = db

class User(BaseModel):
	login = TextField(unique=True)
	password = TextField(unique=True)
	role = TextField(default=Role.CUSTOMER)
	orders = []

class Author(BaseModel):
	name = TextField()
	birthDate = DateTimeField()
	bio = TextField()

class Publisher(BaseModel):
	name = TextField()
	creationDate = DateField()

class Book(BaseModel):
	name = TextField()
	genre = TextField()
	pageCount = IntegerField()
	author = ForeignKeyField(Author)
	publisher = ForeignKeyField(Publisher)
	count = IntegerField()
	price = IntegerField()

class Order(BaseModel):
	bookId = ForeignKeyField(Book)
	userId = ForeignKeyField(User, backref="orders")
	date = DateField(default=date.today())
	
def initDb():
	if not User.table_exists():
		db.create_tables([User, Order, Book, Publisher, Author], safe=True)
	
initDb()
from typing import List

from peewee import *

db = SqliteDatabase("data.db")

class BaseModel(Model):
	class Meta:
		database = db
		
class Book(BaseModel):
	name = TextField()

class User(BaseModel):
	name = TextField()
	age = IntegerField()
	orders: List

class Order(BaseModel):
	user = ForeignKeyField(User, backref="orders")
	book = ForeignKeyField(Book)

if __name__ == '__main__':
	db.create_tables([User, Order, Book], safe=True)
	db.close()
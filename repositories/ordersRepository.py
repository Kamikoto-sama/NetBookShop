from datetime import datetime
from typing import List

from dataBaseContext import Order, User, Book


class OrdersRepository:

	@staticmethod
	def addOrder(userId, bookId) -> dict:
		today = datetime.today().strftime("%d.%m.%Y %H:%M")
		order = Order.create(user=userId, book=bookId, date=today)
		return {"id":order.id, "bookName":order.book.name, "userName":order.user.login, "date":order.date}

	@staticmethod
	def getUserOrders(userId) -> List[dict]:
		user: User = User.select().where(User.id == userId).first()
		orders = list(user.orders.select(Order.id, Book.name.alias("bookName"), Order.date).join(Book).dicts())
		return orders
	
	@staticmethod
	def getOrdersByBookId(bookId) -> list:
		book = Book.select().where(Book.id == bookId).first()
		orders = Order.select().where(Order.book == book).dicts()
		return list(orders)
	
	@staticmethod
	def getAllOrders() -> List[dict]:
		orders = list(Order.select(Order.id, Book.name.alias("bookName"), User.login.alias("userLogin"),
								   Order.date).join(Book, on=(Order.book == Book.id))
					  .join(User, on=(Order.user == User.id)).dicts())
		return orders

	@staticmethod
	def getOrderById(orderId) -> Order:
		order = Order.get(orderId)
		return order

	@staticmethod
	def deleteOrderById(orderId):
		Order.delete_by_id(orderId)
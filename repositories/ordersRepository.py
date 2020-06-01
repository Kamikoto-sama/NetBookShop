from typing import List

from dataBaseContext import Order, User, Book


class OrdersRepository:

	@staticmethod
	def addOrder(userId, bookId) -> Order:
		order = Order.create(userId=userId, bookId=bookId)
		return order

	@staticmethod
	def getUserOrders(userId) -> List[dict]:
		user: User = User.select().where(User.id == userId).first()
		orders = list(user.orders.select(Order.id, Book.name.alias("bookName"), User.login.alias("userName"), 
										 Order.userId, Order.date).join(Book, on=(Order.bookId == Book.id))
					  					.join(User, on=(Order.userId == User.id)).dicts())
		return orders
	
	@staticmethod
	def getAllOrders() -> List[dict]:
		orders = list(Order.select().dicts())
		return orders

	@staticmethod
	def deleteOrderById(orderId):
		Order.delete_by_id(orderId)
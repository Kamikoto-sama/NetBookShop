from typing import Union

from dataBaseContext import User


class UserRepository:
	@staticmethod
	def findUserByLogin(userLogin) -> Union[User, None]:
		user = User.select().where(User.login == userLogin)
		if user.count() == 0:
			return None
		return user.first()
	
	@staticmethod
	def findUserById(userId) -> Union[User, None]:
		user = User.select().where(User.id == userId)
		if user.count() == 0:
			return None
		return user.first()
	
	@staticmethod
	def registerUser(loginData: dict) -> User:
		user = User.create(**loginData)
		return user
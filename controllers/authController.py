from accessCodeProvider import AccessCodeProvider
from controllers.baseController import BaseController
from dataBaseContext import User
from models import Role
from repositories import UserRepository

class AuthController(BaseController):
	def register(self, loginData: dict):
		if not self.validateData(loginData, {"login", "password"}):
			return self.badRequest("Invalid data")
		if UserRepository.findUserByLogin(loginData["login"]) is not None:
			return self.badRequest("This login has already registered")
		if "accessCode" in loginData:
			if loginData["accessCode"] == AccessCodeProvider.accessCode:
				loginData["role"] = Role.LIBRARIAN
			else:
				return self.badRequest("Wrong access code")
		user = UserRepository.registerUser(loginData)
		self.updateUserInfo(user)
		return self.ok(body=user.role)
	
	def login(self, loginData: dict):
		if not self.validateData(loginData, {"login", "password"}):
			return self.badRequest("Invalid data")
		user = UserRepository.findUserByLogin(loginData["login"])
		if user is None:
			return self.badRequest("Invalid login")
		if user.password != loginData["password"]:
			return self.badRequest("Invalid password")			
		
		self.updateUserInfo(user)
		return self.ok(body=user.role)
	
	def updateUserInfo(self, user: User):
		self.userInfo.login = user.login
		self.userInfo.id = user.id
		self.userInfo.role = user.role
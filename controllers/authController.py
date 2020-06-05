from config import accessCode
from controllers.baseController import BaseController
from models import Role
from repositories import UserRepository

class AuthController(BaseController):
	def register(self, loginData: dict):
		if not self.validateData(loginData, {"login", "password"}):
			return self.badRequest("Invalid input data")
		if UserRepository.findUserByLogin(loginData["login"]) is not None:
			return self.badRequest("This login has already registered")
		if "accessCode" in loginData:
			if loginData["accessCode"] == accessCode:
				loginData["role"] = Role.LIBRARIAN
			else:
				return self.badRequest("Wrong access code")
		user = UserRepository.registerUser(loginData)
		return self.ok(body={"role":user.role})
	
	def login(self, loginData: dict):
		if not self.validateData(loginData, {"login", "password"}):
			return self.badRequest("Invalid data")
		user = UserRepository.findUserByLogin(loginData["login"])
		if user is None:
			return self.badRequest("Invalid login")
		if user.password != loginData["password"]:
			return self.badRequest("Invalid password")			
		
		self.userInfo.login = user.login
		self.userInfo.userId = user.id
		self.userInfo.role = user.role
		
		return self.ok(body={"role":user.role})

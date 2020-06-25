import pytest

from accessCodeProvider import AccessCodeProvider
from controllers import *
from dataBaseContext import User
from models import UserInfo, Role


def init():
	User.delete().where(True).execute()
	userInfo = UserInfo(None, 0, None, None)
	controller = AuthController(userInfo, lambda *_: None)
	return controller, userInfo

def test_AuthRegister_registersNewUser():
	controller, userInfo = init()
	loginData = {"login":"login", "password": "pass"}
	
	response = controller.register(loginData)
	
	assert response.succeed
	assert userInfo.login == loginData["login"]
	user = User.select().where(User.login==loginData["login"]).first()
	assert user is not None
	assert user.role == Role.CUSTOMER
	
def test_AuthRegister_registersUsLibrarian_whenAccessCodeProvided():
	controller, userInfo = init()
	loginData = {"login":"login", "password": "pass", "accessCode":AccessCodeProvider.accessCode}

	response = controller.register(loginData)

	assert response.succeed
	assert response.body == Role.LIBRARIAN
	user = User.select().where(User.login==loginData["login"]).first()
	assert user.role == Role.LIBRARIAN
	
def test_AuthLogin_authorizeExistingUser():
	controller, userInfo = init()
	test_AuthRegister_registersNewUser()
	loginData = {"login":"login", "password": "pass"}
	
	response = controller.login(loginData)
	
	assert response.succeed
	assert userInfo.login == loginData["login"]
	assert response.body == Role.CUSTOMER
	
def test_AuthLogin_returnsErrorMessage_whenInvalidData():
	controller, userInfo = init()
	response = controller.login({"login":"kek"})	
	assert not response.succeed
	assert response.errorMessage == "Invalid data"
	
def test_AuthLogin_returnsErrorMessage_whenInvalidLogin():
	controller, userInfo = init()
	response = controller.login({"login":"a", "password":"123"})
	assert not response.succeed
	assert response.errorMessage == "Invalid login"

def test_AuthLogin_returnsErrorMessage_whenInvalidPassword():
	controller, userInfo = init()
	test_AuthRegister_registersNewUser()
	response = controller.login({"login":"login", "password":"123"})
	assert not response.succeed
	assert response.errorMessage == "Invalid password"
	
def test_AuthRegister_returnsErrorMessage_whenSuchLoginRegistered():
	controller, userInfo = init()
	test_AuthRegister_registersNewUser()
	response = controller.register({"login":"login", "password":""})
	assert not response.succeed
	assert response.errorMessage == "This login has already registered"
	
def test_AuthRegister_returnsErrorMessage_whenInvalidAccessCode():
	controller, userInfo = init()
	response = controller.register({"login":"login", "password":"123", "accessCode": "123"})
	assert not response.succeed
	assert response.errorMessage == "Wrong access code"
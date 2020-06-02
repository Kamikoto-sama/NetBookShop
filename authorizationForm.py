from threading import Thread

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox

from clientWorker import ClientWorker
from requestBuilder import RequestBuilder
from ui.convertedUi.authorizationForm import Ui_AuthorizationForm
from models import Response


class AuthForm(Ui_AuthorizationForm, QWidget):
	errorMessageEvent = pyqtSignal(str)
	tryConnectToServerEvent = pyqtSignal(bool)
	serverConnectionLostEvent = pyqtSignal()
	responseReceivedEvent = pyqtSignal(object)

	def __init__(self, clientWorker: ClientWorker, onAuthorized):
		super(QWidget, self).__init__()	
		self.setupUi(self)
		self.clientWorker = clientWorker
		self.onAuthorized = onAuthorized
		self.signInBtn.clicked.connect(self.authenticate)
		self.signUpBtn.clicked.connect(lambda: self.authenticate(True))
		self.accessCodeEdit.hide()
		self.haveAccessCode.stateChanged.connect(self.onHaveAccessCode)
		self.loginEdit.returnPressed.connect(self.authenticate)
		self.passwordEdit.returnPressed.connect(self.authenticate)
		self.accessCodeEdit.returnPressed.connect(self.authenticate)
		
		self.clientWorker.onServerDisconnected = lambda: self.serverConnectionLostEvent.emit()
		self.clientWorker.onError = lambda message: self.errorMessageEvent.emit(message)
		self.errorMessageEvent.connect(self.showErrorMessage)
		self.tryConnectToServerEvent.connect(self.handleServerConnection)
		self.serverConnectionLostEvent.connect(self.onServerConnectionLost)
		self.responseReceivedEvent.connect(self.handleResponse)
		
	def onHaveAccessCode(self, haveAccessCode):
		if haveAccessCode:
			self.accessCodeEdit.show()
			self.accessCodeEdit.setFocus()
		else:
			self.accessCodeEdit.hide()
			
	def onServerConnectionLost(self):
		errorMessage = "Lost connection to the server"
		self.showErrorMessage(errorMessage)
		self.close()

	def init(self):
		self.show()
		tryConnectToServer = lambda: self.tryConnectToServerEvent.emit(self.clientWorker.connectToServer())
		Thread(target=tryConnectToServer).start()

	def handleServerConnection(self, success: bool):
		if not success:
			self.showErrorMessage("Unable to connect to the server")
			self.close()
			return
		self.clientWorker.start()
		self.setEnabled(True)
		self.loginEdit.setFocus()

	def authenticate(self, register=False):
		if not self.validateLoginData():
			return
		loginData = {
			"login": self.loginEdit.text(),
			"password": self.passwordEdit.text(),
		}
		if self.haveAccessCode.checkState():
			loginData["accessCode"] = self.accessCodeEdit.text()
		request = RequestBuilder.Auth.register(loginData) if register else \
					RequestBuilder.Auth.login(loginData)
		responseHandler = lambda response: self.responseReceivedEvent.emit(response)
		self.clientWorker.requestData(request, responseHandler)
	
	def handleResponse(self, response: Response):
		if not response.succeed:
			title = "Invalid data"
			message = response.message
			QMessageBox().warning(self, title, message)
			return
		self.onAuthorized(response.body["role"])

	def validateLoginData(self):
		title = "Invalid login data"
		message = []
		if self.loginEdit.text() == "":
			message = ["Login"]
		if self.passwordEdit.text() == "":
			message.append("Password")
		if self.accessCodeEdit.text() == "" and self.haveAccessCode.checkState():
			message.append("Access code")
		if len(message) > 0:
			message = ", ".join(message) + " required"
			QMessageBox().warning(self, title, message)	
			return False
		return True

	def showErrorMessage(self, message: str):
		QMessageBox().critical(self, "Error", message)
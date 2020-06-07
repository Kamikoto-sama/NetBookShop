from sys import argv

from PyQt5.QtWidgets import QApplication

from authorizationForm import AuthForm
from clientWorker import ClientWorker
from customerForm import CustomerForm
from librarianForm import LibrarianForm
from config import appAddress, appPort
from models import Role


class Main:
	def __init__(self):
		self.clientWorker = ClientWorker(appAddress, appPort)
		self.authForm = AuthForm(self.clientWorker, self.onAuthorized)

	def launch(self):
		self.authForm.init()

	def onAuthorized(self, role):
		if role == Role.CUSTOMER:
			self.customerForm = CustomerForm(self.clientWorker)
			self.customerForm.init()
		elif role == Role.LIBRARIAN:
			self.librarianForm = LibrarianForm(self.clientWorker)
			self.librarianForm.init()
		else:
			message = f"Unknown role {role}"
			print(message)
			self.authForm.showErrorMessage(message)
		self.authForm.close()


if __name__ == '__main__':
	app = QApplication(argv)
	main = Main()
	main.launch()
	app.exec_()

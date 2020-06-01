from controllers import AuthController, CustomerController, LibrarianController

class Controllers:
	Auth = "auth"
	Customer = "user"
	Librarian = "librarian"

	routes = {
		"auth": AuthController,
		"user": CustomerController,
		"librarian": LibrarianController
	}
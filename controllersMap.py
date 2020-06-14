from controllers import AuthController, CustomerController, LibrarianController

class Controllers:
	Auth = "auth"
	Customer = "customer"
	Librarian = "librarian"

	routes = {
		"auth": AuthController,
		"customer": CustomerController,
		"librarian": LibrarianController
	}
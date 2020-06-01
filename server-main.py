from server import Server
from serverTerminal import ServerTerminal

if __name__ == '__main__':
	server = Server().start()
	ServerTerminal(server).start()
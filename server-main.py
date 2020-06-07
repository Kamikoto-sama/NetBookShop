from config import appPort
from server import Server
from serverTerminal import ServerTerminal

if __name__ == '__main__':
	server = Server(port=appPort).start()
	ServerTerminal(server).start()
from config import appPort, appAddress
from server import Server
from serverTerminal import ServerTerminal

if __name__ == '__main__':
    server = Server(appAddress, appPort)
    server.start()
    ServerTerminal(server).start()

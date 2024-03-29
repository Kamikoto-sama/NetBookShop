import socket as Socket
from threading import Thread

from clientHandler import ClientHandler
from logger import Logger
from models import ClientInfo, ChangesEvent, Response

class Server(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.socket = Socket.socket()
        self.socket.bind((address, port))

        self.__isWorking = False
        self.clients = {}
        self.clientIndex = 0

    @property
    def isWorking(self):
        return self.__isWorking

    def run(self):
        self.__isWorking = True
        self.listenClients()

    def listenClients(self):
        while self.__isWorking:
            self.socket.listen()
            clientInfo = self.waitClientConnection()
            if not self.__isWorking:
                return
            self.serveClient(clientInfo)

    def serveClient(self, clientInfo: ClientInfo):
        clientHandler = ClientHandler(clientInfo, self.clientIndex, self.sendChangesUpdateEvent)
        self.clients[self.clientIndex] = clientHandler
        self.clientIndex += 1
        clientHandler.onClientDisconnected = self.onClientDisconnected
        clientHandler.start()

        Logger.log(f"Client #{clientHandler.index} {clientHandler.address} has connected")

    def sendChangesUpdateEvent(self, updateEvent: ChangesEvent):
        client: ClientHandler
        for client in self.clients.values():
            condition = not client.role in updateEvent.roles
            condition = condition and client.userId != updateEvent.includeClientId
            condition = condition or client.index == updateEvent.exceptClientId
            if condition:
                continue
            response = Response(True, "", updateEvent.tables, True)
            client.respond(response.toJson())

    def waitClientConnection(self):
        try:
            clientInfo = self.socket.accept()
            return ClientInfo(clientInfo)
        except OSError:
            if self.__isWorking:
                raise

    def onClientDisconnected(self, client: ClientHandler):
        try:
            self.clients.pop(client.index)
        except KeyError as e:
            Logger.log(f"Error {e} clients={self.clients}")
        Logger.log(f"Client #{client.index} {client.address} has disconnected")

    def stop(self):
        self.__isWorking = False
        self.socket.close()
        client: ClientHandler
        for client in self.clients.values():
            client.pendedToDisconnect = True
            client.disconnect()
        Logger.command("Server has stopped")

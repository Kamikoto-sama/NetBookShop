import socket as Socket
from threading import Thread

from clientHandler import ClientHandler
from logger import Logger
from models import ClientInfo, ChangesEvent, Response


class Server:
	def __init__(self, address="", port=2000):
		self.socket = Socket.socket()
		self.socket.bind((address, port))
		
		self.__isWorking = False
		self.clients = {}

	@property
	def isWorking(self):
		return self.__isWorking

	def start(self):
		self.__isWorking = True
		Thread(target=self.listenClients).start()
		return self
		
	def listenClients(self):
		while self.__isWorking:
			self.socket.listen()
			clientInfo = self.waitClientConnection()
			if not self.__isWorking:
				return
			self.serveClient(clientInfo)
			
	def serveClient(self, clientInfo: ClientInfo):
		clientIndex = len(self.clients)
		clientHandler = ClientHandler(clientInfo, clientIndex, self.sendChangesUpdateEvent)
		self.clients[clientIndex] = clientHandler
		clientHandler.onClientDisconnected = self.onClientDisconnected
		clientHandler.start()

		Logger.log(f"Client #{clientHandler.index} {clientHandler.address} has connected")
	
	def sendChangesUpdateEvent(self, updateEvent: ChangesEvent):
		for client in self.clients.values():
			condition = not client.role in updateEvent.roles
			condition = condition and client.userId != updateEvent.includeClientId
			condition = condition or client.userId == updateEvent.exceptClientId
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
		self.clients.pop(client.index)
		Logger.log(f"Client #{client.index} {client.address} has disconnected")

	def stop(self):
		self.__isWorking = False
		self.socket.close()
		client: ClientHandler
		for client in self.clients.values():
			client.pendedToDisconnect = True
			client.disconnect()
		Logger.command("Server has stopped")
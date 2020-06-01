import socket as Socket
from threading import Thread

from clientHandler import ClientHandler
from models import ClientInfo


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
		clientHandler = ClientHandler(clientInfo, clientIndex)
		self.clients[clientIndex] = clientHandler
		clientHandler.onClientDisconnected = self.onClientDisconnected
		clientHandler.start()

		print(f"\rClient #{clientHandler.clientIndex} {clientHandler.clientAddress} has connected")
	
	def waitClientConnection(self):
		try:
			clientInfo = self.socket.accept()
			return ClientInfo(clientInfo)
		except OSError:
			if self.__isWorking:
				raise
		
	def onClientDisconnected(self, client: ClientHandler):
		self.clients.pop(client.clientIndex)
		print(f"\rClient #{client.clientIndex} {client.clientAddress} has disconnected")

	def stop(self):
		self.__isWorking = False
		self.socket.close()
		for client in self.clients.values():
			client.disconnect()
		print("Server has stopped")
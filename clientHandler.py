from datetime import datetime
from socket import socket
from threading import Thread

from config import dataPackageEncoding, dataClosingSequence, dataPackageSize
from models import ClientInfo
from requestHandler import RequestHandler


class ClientHandler(Thread):
	def __init__(self, clientInfo: ClientInfo, clientIndex):
		super().__init__()
		self.connection: socket = clientInfo.connection
		self.clientAddress = clientInfo.fullAddress 
		self.clientIndex = clientIndex
		self.connectionTime = datetime.now().strftime("%H:%M:%S")
		self.requestHandler = RequestHandler()
		self.onClientDisconnected = lambda *_: None
		
	def disconnect(self):
		self.connection.close()
		
	def run(self):
		requestParts = []
		while receivedData := self.getDataPackage():
			requestParts.append(receivedData.decode(dataPackageEncoding))
			if receivedData.endswith(dataClosingSequence):
				requestData = ''.join(requestParts)[:-len(dataClosingSequence)]
				self.handleRequest(requestData)
				requestParts = []
		self.onClientDisconnected(self)
		
	def getDataPackage(self):
		try:
			return self.connection.recv(dataPackageSize)
		except ConnectionError:
			return 0

	def handleRequest(self, requestData):
		response = self.requestHandler.handle(requestData, self.clientIndex)
		self.respond(response.toJson())

	def respond(self, data: str):
		data = data.encode(dataPackageEncoding) + dataClosingSequence
		self.connection.sendall(data)
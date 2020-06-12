import socket as Socket
from json import JSONDecodeError
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal

from config import dataClosingSequence, dataPackageEncoding, dataPackageSize
from models import Request, Response, ChangesEvent


class ClientWorker(Thread):
	def __init__(self, address, port):
		super().__init__()
		self.address = address
		self.port = port
		self.socket = Socket.socket()
		self.responseQueue = []
		
		self.onError = lambda *_: None
		self.onServerDisconnected = lambda *_: None
		self.onChangesReceived = lambda *_: None

	def run(self):
		self.listenResponse()

	def connectToServer(self):
		try:
			self.socket.connect((self.address, self.port))
		except ConnectionRefusedError:
			return False
		return True
	
	def closeConnection(self):
		self.onServerDisconnected = lambda: None
		self.socket.close()
		
	def listenResponse(self):
		responseParts = []
		while receivedData := self.getDataPackage():
			responseParts.append(receivedData.decode(dataPackageEncoding))
			if receivedData.endswith(dataClosingSequence):
				responseData = ''.join(responseParts)[:-len(dataClosingSequence)]
				self.handleResponse(responseData)
				responseParts = []
		self.onServerDisconnected()

	def getDataPackage(self):
		try:
			return self.socket.recv(dataPackageSize)
		except ConnectionError:
			return 0

	def requestData(self, request: Request, responseCallback):
		requestData = request.toJson().encode(dataPackageEncoding)
		requestData += dataClosingSequence
		self.responseQueue.append(responseCallback)
		self.socket.sendall(requestData)

	def handleResponse(self, responseData: str):
		try:
			response = Response.fromJson(responseData)
		except JSONDecodeError:
			message = f"Invalid data received: {responseData}"
			if responseData.startswith("-m"):
				serverMessage = responseData[2:]
				message = f"Message from server:\n{serverMessage}"
			self.onError(message)
			return 
		if response.changes:
			self.onChangesReceived(response)
		elif len(self.responseQueue) > 0:
			self.responseQueue.pop(0)(response)
		else:
			self.onError(f"Unsupportable response {responseData}")
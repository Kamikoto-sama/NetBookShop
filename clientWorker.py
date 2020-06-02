import socket as Socket
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal

from config import dataClosingSequence, dataPackageEncoding, dataPackageSize
from models import Request, Response


class ClientWorker(Thread):
	def __init__(self, address, port):
		super().__init__()
		self.address = address
		self.port = port
		self.socket = Socket.socket()
		self.responseCallback = None
		
		self.onError = None
		self.onServerDisconnected = None

	def run(self):
		# self.connectToServer()
		self.listenResponse()

	def connectToServer(self):
		try:
			self.socket.connect((self.address, self.port))
		except ConnectionRefusedError:
			return False
		print("Connected")
		return True
		
	def listenResponse(self):
		responseParts = []
		while receivedData := self.getDataPackage():
			responseParts.append(receivedData.decode(dataPackageEncoding))
			if receivedData.endswith(dataClosingSequence):
				responseData = ''.join(responseParts)[:-len(dataClosingSequence)]
				self.handleResponse(responseData)
				responseParts = []
		if self.onServerDisconnected is not None:
			self.onServerDisconnected()

	def getDataPackage(self):
		try:
			return self.socket.recv(dataPackageSize)
		except ConnectionResetError:
			return 0

	def requestData(self, request: Request, responseCallback):
		requestData = request.toJson().encode(dataPackageEncoding)
		requestData += dataClosingSequence
		self.responseCallback = responseCallback
		self.socket.sendall(requestData)

	def handleResponse(self, responseData):
		response = Response.fromJson(responseData)
		if self.responseCallback is not None:
			self.responseCallback(response)
			self.responseCallback = None
			return
		#TODO: Update events
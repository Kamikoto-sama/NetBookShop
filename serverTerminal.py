from sqlite3 import Connection
from threading import Thread

from peewee import SqliteDatabase

from clientHandler import ClientHandler
from logger import Logger
from models import Request


class ServerTerminal(Thread):
	commands: dict

	def __init__(self, server):
		super().__init__()
		self.server = server
		self.bindCommands()

	def bindCommands(self):
		self.commands = {
			'stop': self.server.stop,
			'sql': self.runSql,
			'clients': self.listClients,
			'disconnect': self.disconnectClient,
			'send': self.sendMessageToClient,
			'?': self.showCommands,
			'request': self.makeRequest,
		}
		
	def run(self):
		while self.server.isWorking:
			command = input(">")
			if command == "":
				continue
			self.executeCommand(command)

	def executeCommand(self, command):
		try:
			commandName, *params = command.split()
			if commandName not in self.commands:
				Logger.commandMessage("Unknown command")
				return
			self.commands[commandName](*params)
		except Exception as e:
			Logger.commandMessage(e)
			
	def makeRequest(self, clientIndex, requestRoute: str, body=None):
		if "/" not in requestRoute:
			Logger.commandMessage("Invalid route")
			return
		controller, action = requestRoute.split("/", 1)
		client: ClientHandler = self.getClient(clientIndex)
		if client is None:
			return
		request = Request(controller, action, body)
		response = client.requestHandler.handle(request.toJson(), clientIndex)
		if not response.succeed:
			Logger.commandMessage(response.errorMessage)
		elif response.body is None:
			Logger.commandMessage("No content")
		elif isinstance(response.body, list):
			if len(response.body) > 0:
				[Logger.commandMessage(i) for i in response.body]
			else:
				Logger.commandMessage("No content")
		else:
			Logger.commandMessage(response.body)
		

	def sendMessageToClient(self, clientIndex, message, *messages):
		client = self.getClient(clientIndex)
		if client is None:
			return 
		client.respond(' '.join([message, *messages]))
	
	def disconnectClient(self, clientIndex):
		client = self.getClient(clientIndex)
		if client is None:
			return 
		client.disconnect()
		
	def getClient(self, clientIndex):
		clientIndex = int(clientIndex)
		if not clientIndex in self.server.clients:
			Logger.commandMessage(f"No such client {clientIndex}")
			return
		return self.server.clients[clientIndex]
		
	def showCommands(self):
		Logger.commandMessage("Supported commands:")
		[Logger.commandMessage(command) for command in self.commands if command != "?"]

	def listClients(self):
		clients = self.server.clients.values()
		Logger.commandMessage("Connected clients:" if len(clients) > 0 else "No clients connected")
		client: ClientHandler
		for client in clients:
			Logger.commandMessage(f"#{client.index} {client.role} connected at {client.connectionTime} from {client.address}")

	def runSql(self):
		from dataBaseContext import db
		while 1:
			query = input("sql>")
			if query == "q":
				break
			self.executeSqlQuery(db, query)

	@staticmethod
	def executeSqlQuery(db: SqliteDatabase, query):
		try:
			res = db.execute_sql(query)
		except Exception as e:
			Logger.commandMessage(e)
			return
		if query[:6].lower() in ["select", "pragma"]:
			for row in list(res):
				Logger.commandMessage(row)
		else:
			db.commit()
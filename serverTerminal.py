from sqlite3 import Connection
from threading import Thread

from peewee import SqliteDatabase

from accessCodeProvider import AccessCodeProvider
from clientHandler import ClientHandler
from logger import Logger
from models import Request, ChangesEvent


class ServerTerminal(Thread):
	def __init__(self, server):
		super().__init__()
		self.server = server
		
		self.commands = {
			'stop': self.server.stop,
			'sql': self.runSql,
			'clients': self.runClientShell,
			'disconnect': self.disconnectClient,
			'send': self.sendMessageToClient,
			'?': self.showCommands,
			'request': self.makeRequest,
			'code': self.getAccessCode,
		}
		
	def getAccessCode(self, generateNew = None):
		if generateNew is not None:
			AccessCodeProvider.generateCode()
		Logger.command(AccessCodeProvider.accessCode)

	def run(self):
		while self.server.isWorking:
			Logger.contextPrefix = ""
			command = input(">")
			if command == "":
				continue
			self.executeCommand(command)

	def executeCommand(self, command):
		try:
			commandName, *params = command.split()
			if commandName not in self.commands:
				Logger.command("Unknown command")
				return
			self.commands[commandName](*params)
		except Exception as e:
			Logger.command(e)
			
	def makeRequest(self, clientIndex, requestRoute: str, body=None):
		if "/" not in requestRoute:
			Logger.command("Invalid route")
			return
		controller, action = requestRoute.split("/", 1)
		client: ClientHandler = self.getClient(clientIndex)
		if client is None:
			return
		request = Request(controller, action, body)
		response = client.requestHandler.handle(request.toJson(), clientIndex)
		if not response.succeed:
			Logger.command(response.errorMessage)
		elif response.body is None:
			Logger.command("No content")
		elif isinstance(response.body, list):
			if len(response.body) > 0:
				[Logger.command(i) for i in response.body]
			else:
				Logger.command("No content")
		else:
			Logger.command(response.body)
		
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
			Logger.command(f"No such client {clientIndex}")
			return
		return self.server.clients[clientIndex]
		
	def showCommands(self, commandName=None):
		if commandName is None:
			Logger.command("Supported commands:")
			[Logger.command(command) for command in self.commands if command != "?"]
			return
		if commandName not in self.commands:
			Logger.command("Unknown command")
			return
		commandHandler = self.commands[commandName]
		signature = commandHandler.__func__.__code__.co_varnames[:commandHandler.__func__.__code__.co_argcount]
		params = [param for param in signature if param != "self"]
		message = f"Command params: {', '.join(params)}"
		if len(params) == 0:
			message = f"{commandName} command doesnt accept any params"
		Logger.command(message)
		
	def runClientShell(self, clientIndex=None):
		if clientIndex is None:
			self.listClients()
			return 
		client: ClientHandler = self.getClient(clientIndex)
		if client is None:
			return 
		def req(params):
			if "/" in params:
				Logger.command("Controller name isn't necessary")
				return
			controller = client.role
			action, *body = params.split(" ")
			self.makeRequest(clientIndex, f"{controller}/{action}", *body)
		clientInfo = f"#{client.index} {client.role} connected at {client.connectionTime} from {client.address}"
		commands = {
			"info": lambda: Logger.command(clientInfo),
			"send": lambda message: self.sendMessageToClient(clientIndex, "-m" + message),
			"req": req,
			"?": lambda: [Logger.command(i) for i in commands if i != "?"],
			"-d": lambda: self.disconnectClient(clientIndex),
			"sync": lambda tables: self.sendChangesEvent(clientIndex, *(tables.split()))
		}
		while 1:
			Logger.contextPrefix = f"client#{clientIndex}"
			command = input(f"client#{clientIndex}>")
			commandName, *params = command.split(" ", 1)
			if commandName == "q" or int(clientIndex) not in self.server.clients:
				return
			if commandName == "":
				continue
			if commandName not in commands:
				Logger.command("Unknown command")
				continue
			try:
				commands[commandName](*params)
			except Exception as e:
				Logger.command(e)
				
	def sendChangesEvent(self, clientIndex, table, *tables):
		client: ClientHandler = self.getClient(clientIndex)
		if client is None:
			Logger.command("Unknown client")
			return 
		changesEvent = ChangesEvent([table, *tables], includeClientId=client.userId)
		self.server.sendChangesUpdateEvent(changesEvent)

	def listClients(self):
		clients = self.server.clients.values()
		message = f"Connected clients {len(clients)}:" if len(clients) > 0 else "No clients connected"
		Logger.command(message)
		for client in clients:
			message = f"#{client.index} {client.role} connected at {client.connectionTime} from {client.address}"
			Logger.command(message)

	def runSql(self):
		from dataBaseContext import db
		while 1:
			Logger.contextPrefix = "sql"
			query = input("sql>")
			if query == "q":
				break
			self.executeSqlQuery(db, query)

	@staticmethod
	def executeSqlQuery(db: SqliteDatabase, query):
		try:
			res = db.execute_sql(query)
		except Exception as e:
			Logger.command(e)
			return
		if query[:6].lower() in ["select", "pragma"]:
			for row in list(res):
				Logger.command(row)
		else:
			db.commit()
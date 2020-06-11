from sqlite3 import Connection
from threading import Thread

from peewee import SqliteDatabase

from clientHandler import ClientHandler


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
		}
		
	def sendMessageToClient(self, clientIndex, *message):
		client = self.getClient(clientIndex)
		if client is None:
			return 
		client.respond(' '.join(message))
		
	def disconnectClient(self, clientIndex):
		client = self.getClient(clientIndex)
		if client is None:
			return 
		client.disconnect()
	
	def getClient(self, clientIndex):
		clientIndex = int(clientIndex)
		if not clientIndex in self.server.clients:
			print(f"No such client {clientIndex}")
			return
		return self.server.clients[clientIndex]
		
	def showCommands(self):
		print("Supported commands:")
		[print(command) for command in self.commands if command != "?"]
		
	def listClients(self):
		clients = self.server.clients.values()
		print("Connected clients:" if len(clients) > 0 else "No clients connected")
		client: ClientHandler
		for client in clients:
			print(f"#{client.index} {client.role} connected at {client.connectionTime} from {client.address}")

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
			print(e)
			return
		if query[:6].lower() in ["select", "pragma"]:
			for row in list(res):
				print(row)
		else:
			db.commit()

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
				print("Unknown command")
				return
			self.commands[commandName](*params)
		except Exception as e:
			print(e)

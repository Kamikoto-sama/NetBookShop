from dataclasses import dataclass
from json import JSONDecoder, JSONEncoder
from typing import List


class ClientInfo:
	def __init__(self, rawClientInfo):
		self.connection = rawClientInfo[0]
		rawAddress = rawClientInfo[1]
		self.ipAddress = rawAddress[0]
		self.port = rawAddress[1]
		self.fullAddress = f"{self.ipAddress}:{self.port}"
		
class Request:
	def __init__(self, controller, action, body:dict=None, syncDbChanges = False):
		self.controller = controller
		self.action = action
		self.body = body
		self.syncDbChanges = syncDbChanges
		
	@staticmethod
	def fromJson(requestJson):
		jsonRequest = JSONDecoder().decode(requestJson)
		controller = jsonRequest["controller"]
		action = jsonRequest["action"]
		body = jsonRequest["body"]
		syncDbChanges = jsonRequest["syncDbChanges"]
		return Request(controller, action, body, syncDbChanges)
		
	def toJson(self):
		requestDict = {
			"controller": self.controller,
			"action": self.action,
			"body": self.body,
			"syncDbChanges": self.syncDbChanges
		}
		requestJson = JSONEncoder().encode(requestDict)
		return requestJson
		
class Response:
	def __init__(self, succeed:bool, message:str, body:dict=None, changes:bool=False):
		self.changes = changes
		self.body = body
		self.message = message
		self.succeed = succeed
		
	def toJson(self):
		responseDict = {
			"succeed": self.succeed,
			"message": self.message,
			"changes": self.changes,
			"body": self.body
		}
		responseJson = JSONEncoder().encode(responseDict)
		return responseJson

	@staticmethod
	def fromJson(responseJson):
		jsonResponse = JSONDecoder().decode(responseJson)
		body = jsonResponse["body"]
		message = jsonResponse["message"]
		succeed = jsonResponse["succeed"]
		changes = jsonResponse["changes"]
		return Response(succeed, message, body, changes)
	
class Role:
	CUSTOMER = "customer"
	LIBRARIAN = "librarian"
	NONE = None
	
class ChangesUpdateEvent:
	def __init__(self, tables: List, roles: List=None, exceptClientId=None, includeClientId=None):
		self.includeClientId = includeClientId
		self.roles = roles
		self.tables = tables
		self.exceptClientId = exceptClientId
		
@dataclass
class UserInfo:
	id: int
	login: str
	role: str
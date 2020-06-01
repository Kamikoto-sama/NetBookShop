from models import Role, Response


class BaseController:
	allowedRole = Role.NONE
	
	def __init__(self, userInfo):
		self.userInfo = userInfo

	@staticmethod
	def badRequest(message):
		return Response(False, message)

	@staticmethod
	def ok(message=None, body=None):
		return Response(True, message, body)
	
	@staticmethod
	def validateData(data, requiredParams: set):
		return requiredParams.issubset(set(data))
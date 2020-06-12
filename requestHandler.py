from controllers import BaseController
from controllersMap import Controllers
from logger import Logger
from models import Request, UserInfo


class RequestHandler:
	def __init__(self, changesEvent):
		self.changesEvent = changesEvent
		self.userInfo = UserInfo(None, None, None)
		self.currentController = None

	def handle(self, requestData, clientIndex):
		request = Request.fromJson(requestData)
		Logger.log(f"Client #{clientIndex} requested {request.controller}/{request.action}")
		
		if request.controller not in Controllers.routes:
			message = f"Unknown controller {request.controller}"
			return BaseController.badRequest(message)
		controller = Controllers.routes[request.controller]
		if controller.allowedRole != self.userInfo.role:
			message = f"{request.controller} controller access forbidden with role {self.userInfo.role}"
			return BaseController.badRequest(message)
		if not hasattr(controller, request.action):
			message = f"Unknown action {request.action} of {request.controller} controller"
			return BaseController.badRequest(message)

		if self.currentController is None or not isinstance(self.currentController, controller):
			self.currentController = controller(self.userInfo, self.changesEvent)
		action = getattr(self.currentController, request.action)
		try:
			response = action(request.body) if action.__code__.co_argcount > 1 else action()
		except Exception as e:
			return BaseController.badRequest(str(e))
		return response
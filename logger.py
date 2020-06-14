class Logger:
	contextPrefix = ""
	@staticmethod
	def log(obj):
		print(f"\r{obj}\n{Logger.contextPrefix}>", end="")
		
	@staticmethod
	def command(obj):
		print(f"\r{obj}")
class Logger:
	@staticmethod
	def log(obj):
		print(f"\r{obj}\n>", end="")
		
	@staticmethod
	def commandMessage(obj):
		print(f"\r{obj}")
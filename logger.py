class Logger:
	@staticmethod
	def log(obj):
		print(f"\r{obj}\n>", end="")
		
	@staticmethod
	def command(obj):
		print(f"\r{obj}")
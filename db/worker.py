import MySQLdb

class Worker:
	counter = 0

	def __init__(self, **config):
		self.id = Worker.counter
		Worker.counter += 1
		self.connection = MySQLdb.connect(**config)
		self.connection.autocommit(True)
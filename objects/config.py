import json

class AlreadyReadError(Exception):
	pass

class NotReadError(Exception):
	pass

class Config:
	def __init__(self, file_name="config.json"):
		self.config = {}
		self.default_config = {
			"db": {
				"host": "localhost",
				"username": "admin",
				"password": "melanzana",
				"database": "levbod",
				"connections": 8
			},
			"mirror": {
				"data_path": "data"
			}
		}
		self.file_name = file_name
		self.already_read = False

	def read(self):
		if self.already_read:
			raise AlreadyReadError()
		with open(self.file_name, "r") as f:
			self.config = json.loads(f.read())
		self.already_read = True

	def write_default(self):
		with open(self.file_name, "w") as f:
			f.write(json.dumps(self.default_config))

	def check(self):
		def shape(d):
			if isinstance(d, dict):
				return {k:shape(d[k]) for k in d}
			else:
				return None
		if not self.already_read:
			raise NotReadError()
		return shape(self.config) == shape(self.default_config)

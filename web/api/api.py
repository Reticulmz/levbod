import json

import tornado.gen
import tornado.web
from tornado.escape import json_encode

from objects import exceptions
from web import requests_manager


def args(*required_args):
	"""
	Decorator that checks passed arguments.
	If some arguments are missing, an invalidArgumentsError exception is thrown.
	Example:
	```
	@api.api
	@api.args("first", "second")
	def asyncGet(self):
		...
	```

	:param required_args: tuple containing required arguments strings
	:return:
	"""
	def decorator(function):
		def wrapper(self, *args, **kwargs):
			missing = []
			for i in required_args:
				if i not in self.request.arguments:
					missing.append(i)
			if missing:
				raise exceptions.InvalidArgumentsError("Missing required argument ({})".format(missing))
			return function(self, *args, **kwargs)
		return wrapper
	return decorator

def beautify(f):
	"""
	Handle the `beautify` argument

	:return:
	"""
	def wrapper(self, *args, **kwargs):
		self.beautify = self.get_argument("beautify", None) == "1" or self.get_argument("pretty", None) == "1"
		return f(self, *args, **kwargs)
	return wrapper

def errors(f):
	"""
	Decorator that handles API requests and errors.

	:param f:
	:return:
	"""
	def wrapper(self, *args, **kwargs):
		try:
			return f(self, *args, **kwargs)
		except exceptions.InvalidArgumentsError as e:
			self.data["status"] = 400
			self.data["message"] = str(e)
		except exceptions.ForbiddenError:
			self.data["status"] = 403
			self.data["message"] = "Invalid token"
		except exceptions.NotFoundError:
			self.data["status"] = 404
			self.data["message"] = "Data not found"
		except exceptions.MethodNotAllowedError:
			self.data["status"] = 405
			self.data["message"] = "Method not allowed"
		finally:
			self.set_header("Content-Type", "application/javascript")
			self.set_status(self.data["status"])
			if self.beautify:
				self.write(json.dumps(self.data, indent=4, sort_keys=True))
			else:
				self.write(self.data)
	return wrapper

def api(f):
	"""
	Decorator that handles api errors asynchronously.
	Using this decorator is the same as doing:
	```
	@tornado.gen.engine
	@tornado.web.asynchronous
	@api.errors
	def asyncGet():
		...
	```

	:param f:
	:return:
	"""
	return tornado.gen.engine(tornado.web.asynchronous(beautify(errors(f))))

class AsyncAPIHandler(requests_manager.AsyncRequestHandler):
	"""
	Async API handler.
	Same as a normal asyncRequestHandler, but with a self.data attribute.
	self.data is the dictionary that will be returned in the response.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = {
			"status": 200,
			"message": "ok"
		}
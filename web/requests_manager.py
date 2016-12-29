import tornado
import tornado.web
import tornado.gen
from tornado.ioloop import IOLoop
from objects import glob

class AsyncRequestHandler(tornado.web.RequestHandler):
	def data_received(self, chunk):
		pass

	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self, *args, **kwargs):
		try:
			yield tornado.gen.Task(run_background, (self.async_get, tuple(args), dict(kwargs)))
		finally:
			if not self._finished:
				self.finish()

	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self, *args, **kwargs):
		try:
			yield tornado.gen.Task(run_background, (self.async_post, tuple(args), dict(kwargs)))
		finally:
			if not self._finished:
				self.finish()

	def async_get(self, *args, **kwargs):
		self.send_error(405)
		self.finish()

	def async_post(self, *args, **kwargs):
		self.send_error(405)
		self.finish()

	def get_ip(self):
		if "CF-Connecting-IP" in self.request.headers:
			return self.request.headers.get("CF-Connecting-IP")
		elif "X-Forwarded-For" in self.request.headers:
			return self.request.headers.get("X-Forwarded-For")
		else:
			return self.request.remote_ip

def run_background(data, callback):
	func, args, kwargs = data
	def _callback(result):
		IOLoop.instance().add_callback(lambda: callback(result))
	glob.pool.apply_async(func, args, kwargs, _callback)
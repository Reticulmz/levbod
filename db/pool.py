import gevent.queue
import gevent.greenlet
import MySQLdb

from db import worker

class Pool:
	def __init__(self, max_size, **config):
		self.workers = gevent.queue.Queue(max_size)
		self.config = config
		self.fill()

	def fill(self):
		for i in range(0, self.workers.maxsize - len(self.workers)):
			self.workers.put_nowait(worker.Worker(**self.config))

	def get_worker(self):
		return self.workers.get()

	def put_worker(self, work):
		self.workers.put_nowait(work)

	def execute(self, query, params=None):
		if params is None:
			params = ()
		cursor = None
		work = self.get_worker()
		try:
			cursor = work.connection.cursor()
			cursor.execute(query, params)
			work.connection.commit()
		finally:
			if cursor is not None:
				cursor.close()
			self.put_worker(work)

	def fetch(self, query, params=None, _all=False):
		if params is None:
			params = ()
		cursor = None
		work = self.get_worker()
		try:
			cursor = work.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(query, params)
			data = cursor.fetchone() if not _all else cursor.fetchall()
			return data
		finally:
			if cursor is not None:
				cursor.close()
			self.put_worker(work)

	def fetch_all(self, query, params=None):
		return self.fetch(query, params, True)
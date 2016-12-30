from web.api import api
from objects import glob
from objects import exceptions

class Handler(api.AsyncAPIHandler):
	@api.api
	@api.args("id")
	def async_get(self, *args, **kwargs):
		try:
			beatmapset_id = int(self.get_argument("id"))
		except (TypeError, ValueError):
			raise exceptions.InvalidArgumentsError()

		beatmapset_data = glob.db.fetch("SELECT * FROM beatmapsets WHERE beatmapset_id = %s LIMIT 1", [beatmapset_id])
		if beatmapset_data is None:
			raise exceptions.NotFoundError()

		self.data["data"] = {
			"beatmapset_id": beatmapset_id,
			"artist": beatmapset_data["artist"],
			"title": beatmapset_data["title"],
			"creator": beatmapset_data["creator"],
			"ranked_status": beatmapset_data["ranked_status"],
		}
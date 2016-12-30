from web.api import api
from objects import glob
from objects import exceptions

class Handler(api.AsyncAPIHandler):
	@api.api
	@api.args("id")
	def async_get(self, *args, **kwargs):
		try:
			beatmap_id = int(self.get_argument("id"))
		except (TypeError, ValueError):
			raise exceptions.InvalidArgumentsError()

		beatmap_data = glob.db.fetch("SELECT beatmapset_id FROM child_beatmaps WHERE beatmap_id = %s LIMIT 1", [beatmap_id])
		if beatmap_data is None:
			raise exceptions.NotFoundError()
		beatmapset_data = glob.db.fetch("SELECT * FROM beatmapsets WHERE beatmapset_id = %s LIMIT 1", [beatmap_data["beatmapset_id"]])
		if beatmapset_data is None:
			raise exceptions.NotFoundError()

		self.data["data"] = {
			"beatmapset_id": beatmap_data["beatmapset_id"],
			"artist": beatmapset_data["artist"],
			"title": beatmapset_data["title"],
			"creator": beatmapset_data["creator"],
			"ranked_status": beatmapset_data["ranked_status"],
		}
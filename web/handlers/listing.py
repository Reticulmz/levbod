from web.api import api
from objects import glob
from utils import mirror

class Handler(api.AsyncAPIHandler):
	@api.api
	def async_get(self, *args, **kwargs):
		try:
			mode = int(self.get_argument("mode", None))
			if mode < 0 or mode > 3:
				mode = None
		except (ValueError, TypeError):
			mode = None

		self.data["data"] = []
		sets = glob.db.fetch_all("SELECT * FROM beatmapsets ORDER BY last_update DESC LIMIT 10")
		for set in sets:
			self.data["data"].append({
				"beatmapset_id": set["beatmapset_id"],
				"artist": set["artist"],
				"title": set["title"],
				"creator": set["creator"],
				"ranked_status": int(set["ranked_status"]),
				"beatmaps": []
			})

			diffs = glob.db.fetch_all("SELECT DISTINCT beatmap_id FROM child_beatmaps WHERE beatmapset_id = %s LIMIT 10", [set["beatmapset_id"]])
			for diff in diffs:
				beatmap_data = mirror.get_beatmap(diff["beatmap_id"])
				if beatmap_data is None:
					continue

				self.data["data"][-1]["beatmaps"].append({
					"beatmap_id": diff["beatmap_id"],
					"difficulty_name": beatmap_data["DiffName"],
					"game_mode": beatmap_data["Mode"],
				})
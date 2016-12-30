from web.api import api
from objects import glob
from utils import mirror

BEATMAPS_PER_PAGE = 100

class Handler(api.AsyncAPIHandler):
	@api.api
	def async_get(self, *args, **kwargs):
		# Return data is a list
		self.data["data"] = []

		# Get game mode filter
		# set mode to -1 mode filter is disabled
		try:
			mode = int(self.get_argument("mode", -1))
			if mode < -1 or mode > 3:
				mode = -1
		except (ValueError, TypeError):
			mode = -1

		# Get page (starts from 0)
		try:
			page = int(self.get_argument("page", 0))
		except (ValueError, TypeError):
			page = 0

		# Get osu!direct ranked status
		try:
			ranked_status = int(self.get_argument("status", 0))
		except (ValueError, TypeError):
			ranked_status = 0

		# Get query
		search_query = self.get_argument("query", "")

		# Convert osu!direct ranked status to osu!api ranked status
		ranked_status_db = 1
		if ranked_status == 0 or ranked_status == 7:
			ranked_status_db = 1
		elif ranked_status == 8:
			ranked_status_db = 4
		elif ranked_status == 3:
			ranked_status_db = 3
		elif ranked_status == 2:
			ranked_status_db = 0
		elif ranked_status == 5:
			ranked_status_db = -2
		elif ranked_status == 4:
			ranked_status_db = None

		# Fetch all beatmap sets from db that match our ranked status, page and query
		sets = glob.db.fetch_all("SELECT * FROM beatmapsets WHERE {} = %(ranked_status)s AND (title LIKE %(query)s OR artist LIKE %(query)s OR creator LIKE %(query)s OR source LIKE %(query)s) ORDER BY last_update DESC LIMIT %(beatmaps_per_page)s OFFSET %(offset)s".format(
			1 if ranked_status_db is None else "ranked_status"
		), {
			"ranked_status": ranked_status_db if ranked_status_db is not None else 1,
			"beatmaps_per_page": BEATMAPS_PER_PAGE,
			"query": "%{}%".format(search_query),

			"page": page,
			"offset": BEATMAPS_PER_PAGE * page,
		})

		# Process each set
		for set in sets:
			# Append the current set to data
			self.data["data"].append({
				"beatmapset_id": set["beatmapset_id"],
				"artist": set["artist"],
				"title": set["title"],
				"creator": set["creator"],
				"ranked_status": int(set["ranked_status"]),
				"beatmaps": []  # set difficulties list to empty
			})

			# If we are not filtering by mode, always include every set
			include_set = mode == -1

			# Fetch the difficulties from the db
			diffs = glob.db.fetch_all("SELECT DISTINCT beatmap_id FROM child_beatmaps WHERE beatmapset_id = %s LIMIT %s", [set["beatmapset_id"], BEATMAPS_PER_PAGE])

			# Process each difficulty
			for diff in diffs:
				# Read beatmap info json file from the static mirror
				beatmap_data = mirror.get_beatmap(diff["beatmap_id"])

				# If there was an error while reading the difficulty info file
				# Set this difficulty yo Unknown@osu!standard
				if beatmap_data is None:
					beatmap_data = {
						"DiffName": "Unknown",
						"Mode": 0
					}

				# If we are filtering by mode and we aren't sure if we should
				# include this set in the results list yet, check if this diff
				# matches the mode filter, if so, include this set
				if not include_set:
					if beatmap_data["Mode"] == mode:
						include_set = True

				# Append this diff to the last set in the results list
				self.data["data"][-1]["beatmaps"].append({
					"beatmap_id": diff["beatmap_id"],
					"difficulty_name": beatmap_data["DiffName"],
					"game_mode": beatmap_data["Mode"],
				})

			# If we are filtering by mode and this beatmap doesn't have any beatmap
			# that match our mode, recreate the list removing the last item (current beatmap)
			if not include_set:
				self.data["data"] = self.data["data"][:-1]
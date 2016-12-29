import threading
import sys

import strict_rfc3339

from objects import glob
from db import pool
from utils import console
from objects import config
from utils import mirror

WORKERS = 48
total_maps = 0

class Worker:
	id = 1

	def __init__(self, data):
		self.data = data
		self.id = Worker.id
		self.thread = None
		Worker.id += 1

	def work(self):
		global total_maps

		# Process all assigned betamap sets
		for set in self.data:
			# Output every 1000 maps
			if total_maps % 1000 == 0:
				print("[W{}] Processed {} sets".format(self.id, total_maps))

			# Add set to db
			glob.db.execute(
				"INSERT INTO beatmapsets (id, beatmapset_id, ranked_status, last_update, artist, title, creator, source, tags, has_video)"
				"VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
				[set["SetID"], set["RankedStatus"], strict_rfc3339.rfc3339_to_timestamp(set["LastUpdate"]), set["Artist"], set["Title"], set["Creator"],
				 set["Source"], set["Tags"], 1 if set["HasVideo"] == "true" else 0])

			# Add child beatmaps to db
			for beatmap in set["ChildrenBeatmaps"]:
				glob.db.execute("INSERT INTO child_beatmaps (id, beatmap_id, beatmapset_id) VALUES (NULL, %s, %s)", [beatmap, set["SetID"]])

			total_maps += 1

if __name__ == "__main__":
	# Load config
	console.print_n("> Reading config.json...")
	glob.config = config.Config()
	glob.config.read()
	console.done()

	# Connect to db
	console.print_n("> Connecting to db...")
	db_config = glob.config.config["db"]
	glob.db = pool.Pool(max_size=WORKERS,
	                    host=db_config["host"],
						user=db_config["username"],
						passwd=db_config["password"],
						db=db_config["database"],
						charset="utf8mb4")
	console.done()

	# Read index.json
	print("Reading index.json...")
	data = mirror.get_index()
	if data is None:
		print("Couldn't read index.json")
		sys.exit()
	glob.db.execute("TRUNCATE TABLE beatmapsets")

	# Spawn workers
	workers = []
	start = 0
	step = int(len(data) / WORKERS)
	for i in range(0, WORKERS):
		# Create a Worker object, create its thread and start it
		w = Worker(data[start:start + step])
		w.thread = threading.Thread(target=w.work)
		workers.append(w)
		w.thread.start()
		start += step

	# Wait until all workers finish their work
	for i in workers:
		i.thread.join()
		print("Worker {} has finished its work".format(i.id))
	print("Done!")
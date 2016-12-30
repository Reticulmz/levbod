import json
import codecs

from objects import glob

def get_data_folder():
	return glob.config.config["mirror"]["data_path"]

def get_beatmap(beatmap_id):
	try:
		with codecs.open("{}/b/{}.json".format(get_data_folder(), beatmap_id), "r", "utf-8") as f:
			data = json.loads(f.read())
		data["Mode"] = int(data["Mode"])
	except (json.JSONDecodeError, ValueError, FileNotFoundError):
		data = None
	return data

def get_index():
	try:
		with codecs.open("{}/index.json".format(get_data_folder()), "r", "utf-8") as f:
			data =  json.loads(f.read())
	except (json.JSONDecodeError, ValueError, FileNotFoundError):
		data = None
	return data
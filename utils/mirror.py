import json

from objects import glob

def get_data_folder():
	return glob.config.config["mirror"]["data_path"]

def get_beatmap(beatmap_id):
	try:
		with open("{}/b/{}.json".format(get_data_folder(), beatmap_id), "r") as f:
			data =  json.loads(f.read())
	except (json.JSONDecodeError, ValueError, FileNotFoundError):
		data = None
	return data

def get_index():
	try:
		with open("{}/index.json".format(get_data_folder()), "r") as f:
			data =  json.loads(f.read())
	except (json.JSONDecodeError, ValueError, FileNotFoundError):
		data = None
	return data
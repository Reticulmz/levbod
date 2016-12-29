import requests
import json

BASE_URL = "http://storage.ripple.moe"

def api_request(type, id):
	result = requests.get("{}/{}/{}.json".format(BASE_URL, type, id))
	if result.status_code != 200:
		return None
	return json.loads(result.text)

def get_beatmap(beatmap_id):
	return api_request("b", beatmap_id)

def get_beatmapset(beatmapset_id):
	return api_request("s", beatmapset_id)
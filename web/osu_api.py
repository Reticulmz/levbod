import requests
import json

from objects import glob

BASE_URL = "http://osu.ppy.sh/api"

def get_api_url(handler):
	return "{}/{}".format(BASE_URL, handler)

def api_request(handler, params=None, token=None):
	if token is None:
		token = glob.osu_api_key
	if params is None:
		params = {}
	params["k"] = token
	result = requests.get(get_api_url(handler), params=params)
	return json.loads(result.text)

def get_beatmapset(beatmapset_id):
	return api_request("get_beatmaps", {
		"s": beatmapset_id
	})

def get_beatmaps(mode=None, limit=100):
	params = {
		"limit": limit
	}
	if mode is not None:
		params["m"] = mode
	return api_request("get_beatmaps", params)
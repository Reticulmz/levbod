import sys
from multiprocessing.pool import ThreadPool

import tornado.ioloop

from web.handlers import listing
from web.handlers import beatmapset
from web.handlers import beatmap
from db import pool
from objects import glob
from utils import console
from constants import bcolors
from objects import config

console.colored(""" _         _         _
| |___ _ _| |_ ___ _| |
| | -_| | | . | . | . |
|_|___|\_/|___|___|___|
""", bcolors.BLUE)

console.colored("""Le very basic osu!direct
A temporary osu!direct api
When bloodcat goes offline
""", bcolors.GREEN)

console.colored("""Use this until ~01/01/2017,
then Howl will release a new
mirror with api and everything
""", bcolors.YELLOW)

console.print_n("> Reading config.json...")
glob.config = config.Config()
try:
	glob.config.read()
except FileNotFoundError:
	print("\nconfig.json doesn't exist. Generating a default one..")
	glob.config.write_default()
	sys.exit()
console.done()

console.print_n("> Connecting to db...")
db_config = glob.config.config["db"]
glob.db = pool.Pool(max_size=db_config["connections"],
                    host=db_config["host"],
					user=db_config["username"],
					passwd=db_config["password"],
					db=db_config["database"],
					charset="utf8mb4")
console.done()

print("> Web server started on 0.0.0.0:{}".format(glob.config.config["server"]["port"]))
glob.pool = ThreadPool(glob.config.config["server"]["threads"])
tornado.web.Application([
	(r"/listing", listing.Handler),
	(r"/beatmapset", beatmapset.Handler),
	(r"/beatmap", beatmap.Handler),
]).listen(glob.config.config["server"]["port"])
tornado.ioloop.IOLoop.instance().start()
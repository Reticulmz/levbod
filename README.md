## Levbod
### Le very basic osu!direct
#### A temporary osu!direct api when bloodcat goes offline

- Origin: https://git.zxq.co/ripple/levbod
- Mirror: https://github.com/osuripple/levbod


This software is an api with osu!direct features that can be used with the [ripple static mirror](https://git.zxq.co/ripple/mirror).
`index.json`'s content is saved in a MySQL database, for performance reasons, and info of single beatmaps is read from the json files in `b/` mirror's data folder.

### Requirements
- A MySQL server
- Python 3.5
- A working [ripple static mirror](https://git.zxq.co/ripple/mirror).
- Some Python dependencies

### Installation
- Make sure the mirror has downloaded all the beatmaps and it has created all the json files
- Create an empty MySQL database (and user)
- Import `schema.sql` in your database
```
$ mysql -u levbod -p levbod < schema.sql
```
- Install levbod's dependencies using `pip`
```
$ pip install -r requirements.txt
```
- Start levbod once to create a default config file and edit it
```
$ python3 levbod.py
$ nano config.json
...
```
- Put `index.json` data in the database using `convert.py` (this might take a while depending on your disk speed)
```
$ python3 convert.py
```
- Start the api server
```
$ python3 levbod.py
```

### Nginx config
Optionally, you can configure nginx as a reverse proxy:
```
server {
    listen 80;
    server_name storage.ripple.moe;
    charset utf-8;

    # Ripple static mirror
    location ~ \.osz$ {
        add_header Content-Disposition 'attachment;filename="$basename";';
    }

    # Levbod reverse proxy
    location /levbod {
        rewrite ^/levbod/(.*) /$1  break;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:5588$uri$is_args$args;
    }
}
```

### [API Documentation](http://docs.ripple.moe/docs/levbod/api)

### LICENSE
All code in this repository is licensed under the GNU AGPL 3 License.
See the "LICENSE" file for more information
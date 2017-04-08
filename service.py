from base64 import b64decode

from flask import Flask
from werkzeug.contrib.cache import SimpleCache

import config
from rebuild import rebuild_page


app = Flask(__name__, static_folder='static')
cache = SimpleCache()


@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/fog/<source>/<target>')
def rebuilding_page(source, target):
    source_url = b64decode(source).decode()
    target_url = b64decode(target).decode()

    cache_key = source_url + target_url
    cached_page = cache.get(cache_key)
    if cached_page:
        return cached_page

    page = rebuild_page(source_url, target_url)
    if page:
        cache.set(cache_key, page, timeout=6 * 60 * 60)
        return page

    return 'failed rendering page', 404


if __name__ == '__main__':
    app.run(host=config.host, port=config.port)

import logging
import sys
import laundry_scraper
from flask import Flask, jsonify
from flask.ext.cache import Cache


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config.from_object('default_config')

app.logger.addHandler(logging.StreamHandler(sys.stdout))

@cache.cached(timeout=30)
@app.route('/all')
def scrape_all():
    response = laundry_scraper.scrape_all()
    return jsonify(response)

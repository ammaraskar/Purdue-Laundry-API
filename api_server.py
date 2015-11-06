import logging
import sys
import laundry_scraper
from flask import Flask, jsonify
from werkzeug.contrib.cache import SimpleCache


app = Flask(__name__)
cache = SimpleCache()

app.config.from_object('default_config')

app.logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/all')
def scrape_all():
    response = cache.get('laundry-response')
    if response is None:
        response = jsonify(laundry_scraper.scrape_all())
        cache.set('laundry-response', response, 30)
    return response

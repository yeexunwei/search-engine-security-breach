#!/usr/bin/env python

import flask
from flask import request, jsonify
import lucene2 as lucene

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# ===========================================================================================================

@app.route('/api/search', methods=['GET'])
def search_term():
    if 'term' in request.args:
        term = str(request.args['term'])
    else:
        return "Error: No search field provided. Please specify a search term."

    results = lucene.search(term)
    # return results
    return jsonify(results)

@app.route('/api/rating', methods=['GET', 'POST'])
def add_rating():
    if 'rate' in request.args:
        rate = int(request.args['rate'])
    else:
        return "Error: No rating field provided. Please specify a rating term."
    if 'number' in request.args:
        number = int(request.args['number'])
    else:
        return "Error: No number field provided. Please specify a number term."
    if 'term' in request.args:
        term = str(request.args['term'])
    else:
        return "Error: No search field provided. Please specify a search term."
    
    lucene.save_rating(term, number, rate)
    return flask.redirect("http://127.0.0.1:5001/search/" + term)


app.run()
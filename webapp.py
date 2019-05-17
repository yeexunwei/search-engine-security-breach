#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for
from forms import SearchForm, Form1, Form2
import requests
import json
import flask
from flask import request, jsonify
import lucene as lucene
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'

# =========================================== Main Class ========================================================

class LuceneMain():
    def __init__(self):
        path = 'cyber-security-breaches-data/Cyber Security Breaches.csv'
        self.df = pd.read_csv(path)
        self.df.dropna(subset=['Summary'], inplace=True)
        self.df.drop_duplicates(subset='Name_of_Covered_Entity', keep='first', inplace=True)
        self.df.rename(columns={'Unnamed: 0':'Index'}, inplace=True)
        
        self.ix = lucene.create_index(self.df)
        
    def search(self, query_str):
        results = lucene.search(query_str=query_str, ix=self.ix, df=self.df)
        return results

    def search_info(self, query_str):
        results = lucene.search(query_str=query_str, ix=self.ix, df=self.df, result_type='info')
        return results
    
    def save_rating(self, query_str, number, rating):
        # return jsonify({'query' : query_str, 'number' : number, 'rating' : rating})
        self.df = lucene.save_rating(query_str, number, rating, self.df)
        return

security_breach = LuceneMain()

# =========================================== WEB ================================================================

@app.route('/', methods=['GET', 'POST'])
def home():
	form = SearchForm()
	if form.validate_on_submit():
		return redirect(url_for('search', name=form.username.data))
	return render_template('search.html', form=form)


@app.route('/search/<name>')
def search(name):
    info = requests.get("http://127.0.0.1:5000/api/search?term=" + name)
    info = json.loads(info.text)

    basic_info = requests.get("http://127.0.0.1:5000/api/searchinfo?term=" + name)
    basic_info = json.loads(basic_info.text)

    if info is None:
        return render_template('noresult.html')

    form1 = Form1()
    if form1.submit1.data and form1.validate():
        return redirect(url_for('add_rating'))

    return render_template('show.html', info=info, term=name, form1=form1, basic=basic_info)
   # return info.text

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/show', methods=['GET', 'POST'])
def show():
    result = request.form
    return jsonify(result)

# =========================================== API ================================================================

@app.route('/api/searchinfo', methods=['GET'])
def search_info():
    if 'term' in request.args:
        term = str(request.args['term'])
    else:
        return "Error: No search field provided. Please specify a search term."

    results = security_breach.search_info(term)
    return jsonify(results)

#              SEARCH
@app.route('/api/search', methods=['GET'])
def search_term():
    if 'term' in request.args:
        term = str(request.args['term'])
    else:
        return "Error: No search field provided. Please specify a search term."

    results = security_breach.search(term) 
    return jsonify(results)

#              RATING
@app.route('/api/rating', methods=['GET', 'POST'])
def add_rating():
    if 'rate' in request.form:
        rate = int(request.form['rate'])
    else:
        return "Error: No rating field provided. Please specify a rating term."
    if 'number' in request.form:
        number = int(request.form['number'])
    else:
        return "Error: No number field provided. Please specify a number term."
    if 'term' in request.form:
        term = str(request.form['term'])
    else:
        return "Error: No search field provided. Please specify a search term."
    
    security_breach.save_rating(term, number, rate)
    return redirect(url_for('search', name=term))

if __name__ == '__main__':
   app.run(debug=True, host='127.0.0.1', port=5000)
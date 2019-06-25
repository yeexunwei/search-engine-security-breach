# Lucene Search Engine with Relevance Feedback

Information retrieval system of Cyber Security Breaches Data. Implemented using Lucene.

Rating system is provided for user to provide feedback to improve the ranking.

## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
# flask
pip install flask

# whoosh
pip install whoosh
```

## Deployment

```
export FLASK_APP=webapp.py
flask run
```
http://127.0.0.1:5000/search/security
http://127.0.0.1:5000/api/search?term=breach

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Whoosh](https://bitbucket.org/mchaput/whoosh/wiki/Home) - Lucene library implementation


## Acknowledgments

* [Cyber Security Breaches Data](https://www.kaggle.com/alukosayoenoch/cyber-security-breaches-data/version/1)

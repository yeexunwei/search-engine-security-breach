#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import sys
import json
import numpy as np
from math import log10
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, DATETIME, COLUMN, NUMERIC
from whoosh.columns import VarBytesColumn, NumericColumn
from whoosh.writing import AsyncWriter

from whoosh.qparser import QueryParser, OrGroup, MultifieldParser, OperatorsPlugin
from whoosh import scoring
from whoosh.index import open_dir

from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.analysis import StandardAnalyzer, StemmingAnalyzer

# ============================================= Index ==============================================

def createSearchableData(df):
    my_analyzer=StemmingAnalyzer()

    # schema definition
    schema = Schema(number=ID(stored=True),
                    entity=TEXT(stored=True, field_boost=3.0, analyzer=my_analyzer, sortable=True),
                    type_breach=TEXT(stored=True, field_boost=2.0, analyzer=my_analyzer, sortable=True),
                    summary=TEXT(stored=True, analyzer=my_analyzer, sortable=True),
                    summary_text=TEXT(stored=True)
                   )
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    
    # creating an index writerto add doc
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    
    def index_df(row):
        writer.update_document(number=str(row['Number']),
                               entity=row['Name_of_Covered_Entity'],
                               type_breach=row['Type_of_Breach'],
                               summary=row['Summary'],
                               summary_text=row['Summary']
                              )
        return None
                               
    df.apply(index_df, axis=1)
    writer.commit()
    return None

def create_index(df):
    createSearchableData(df)
    ix = open_dir("indexdir")
    return ix

# ============================================= Results ==============================================

def show_results(results):
    for hit in results:
        print(hit['number'], hit["entity"])
        print(hit["summary"])
        print()
    return None

def tokenise(query_str):
    tokenizer = StemmingAnalyzer()
    new_term = ''
    for token in tokenizer(query_str):
        new_term += token.text + ' '
    new_term = new_term[:-1]
    return new_term

# dict
def get_search_info(search_results):
    keywords = [keyword for keyword, score in search_results.key_terms("summary", docs=10, numterms=5)]

    info = {"showing" : search_results.scored_length(), "total" : len(search_results), "keywords" : keywords}
    return info

def get_average_rating(rating_lst):
    average_rating = 0
    if len(rating_lst) != 0:
        average_rating = sum(rating_lst) / len(rating_lst)
        average_rating = round(average_rating, 1)
    return average_rating

def get_max(term, df):
    max_lst = df[term].apply(len).max(axis=0)
    return max_lst

def get_boost(score, average_rating, rate_n, max_score, max_n):
    tf_score = (log10(10 + score) / log10(10 + max_score))
    n_score = (log10(10 + rate_n) / log10(10 + max_n)) # more people vote
    rating_score = (log10(10 + average_rating) / log10(10 + 5)) # normalise rating
    priority = n_score * rating_score

    new_score = 0.9 * tf_score + 0.1 * priority
    return new_score

def calculate_new_rating(query_str, df, search_results):
    # calculate new score with relevance feedback
    result_table = pd.DataFrame(columns=['Score', 'NewScore', 'Number', 'Entity', 'Type', 'Summary', 'Highlight'])
    term = tokenise(query_str)
    max_score = search_results[0].score

    if term in df.columns[11:]:
        max_n = get_max(term, df)
    else:
        df[term] = np.empty((len(df), 0)).tolist()
        max_n = 0
        
    for result in search_results:
        rating_lst = df.at[int(result['number']), term]
        rate_n = len(rating_lst)
        average_rating = get_average_rating(rating_lst)

        # new_score = result.score
        new_score = get_boost(result.score, average_rating, rate_n, max_score, max_n)
        
        new_row = { 'Score' : round(result.score, 2),
                   'NewScore' : round(new_score, 4),
                   'Rating' : str(average_rating) + ' / ' + str(rate_n),
                   'Number' : result['number'],
                   'Entity' : result['entity'],
                   'Type' : result['type_breach'],
                   'Summary' : result['summary'],
                   'Highlight' : result.highlights('summary')}
        result_table = result_table.append(new_row, ignore_index=True)

    result_table = result_table.sort_values(['NewScore'], ascending=False)
    results = []
    for jdict in result_table.to_dict(orient='records'):
        results.append(jdict)

    return results

def search(query_str, ix, df, result_type='all'):
    topN = 10
    sortedby = None
    # weigthing = scoring.BM25F()
    weighting=scoring.TF_IDF()

    with ix.searcher(weighting=weighting) as searcher:
        mparser = MultifieldParser(["entity", "type_breach", "summary"], ix.schema)
        query = mparser.parse(query_str)
        search_results = searcher.search(query,limit=topN, sortedby=sortedby)

        if len(search_results) == 0:
            return None

        if result_type == 'info':
            return get_search_info(search_results)
        return calculate_new_rating(query_str, df, search_results)
     
def save_to_csv(df):
    df.to_csv('cyber-security-breaches-data/Cyber Security Breaches.csv')
    return

# ============================================= Rating ==============================================
def save_rating(query_str, number, rating, df):
    new_term = tokenise(query_str)
    df.at[number, new_term] += [int(rating)]
    return df
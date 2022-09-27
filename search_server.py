import os
import json
import flask
import logging
import numpy as np
from time import time
from uuid import uuid4
from flask import request
from pprint import pprint
import tensorflow_hub as hub
from qdrant_client import QdrantClient


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = flask.Flask('arxiv-search')


base_html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>Literature Review Bot</title>
</head>
<body>
<h1>arXiv Semantic Search</h1>
<label for="search">Search query. Format it like a title and/or abstract similar to what you're looking for.</label>
<form action="http://127.0.0.1/" method="post">
<input type="text" placeholder="Abstract" name="search" size="180">
<button type="submit">Search</button>
</form>
'''

html_close = '''
</body>
</html>
'''


@app.route('/', methods=['POST', 'GET'])
def home():
    if flask.request.method == 'GET':
        return base_html + html_close
    elif flask.request.method == 'POST':
        start = time()
        query = flask.request.form['search']
        print('Query received:', query)
        embeddings = embed([query])
        vectors = embeddings.numpy().tolist()
        results = client.search(
            collection_name='arxiv',
            query_vector=vectors[0],
            limit=10)
        #pprint(results)
        html = base_html + '<p>Query time: %s seconds</p>' % (time() - start)
        html = html + '<p>Search query: %s</p>' % query
        for result in results:
            html = html + '<h2><a href="https://arxiv.org/abs/%s" target="_blank">%s</a></h2>' % (result.payload['id'], result.payload['title'])
            html = html + '<p>Score: <b>%s</b></p>' % result.score
            html = html + '<blockquote>%s</blockquote>' % result.payload['abstract']
            html = html + html_close
        return html



if __name__ == '__main__':
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")  # USEv5 is about 100x faster than 4
    client = QdrantClient(host='localhost', port=6333)
    app.run(host='0.0.0.0', port=80)
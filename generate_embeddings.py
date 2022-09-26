import os
import json
import tensorflow_hub as hub
import textwrap
import re
from uuid import uuid4
from time import time


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_data(directory, payload):
    filename = '%s.json' % str(uuid4())
    with open('%s/%s' % (directory, filename), 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=1)


def process_chunk(chunk):
    try:
        articles = list()
        strings = list()
        for article in chunk:
            info = json.loads(article)
            title = re.sub('\s+', ' ', info['title'].strip())
            #print(title)
            abstract = re.sub('\s+', ' ', info['abstract'].strip())
            string = title + ' ' + abstract
            articles.append({'id':info['id'], 'title':title, 'abstract':abstract})
            strings.append(string)    
        embeddings = embed(strings)  # try to do 100 embeddings at a time
        vectors = embeddings.numpy().tolist()
        for i in list(range(0, len(chunk))):
            article = articles[i]
            article['embedding'] = vectors[i]
            save_data('embeddings', article)
    except Exception as oops:
        print(oops)
        save_data('errors', chunk)


if __name__ == '__main__':
    embed = hub.load('https://tfhub.dev/google/universal-sentence-encoder-large/5')
    arxiv = open_file('c:/arxiv/arxiv-metadata-oai-snapshot.json').splitlines()
    print('Articles loaded:', len(arxiv))
    chunk_size = 300
    chunks = [arxiv[i:i + chunk_size] for i in range(0, len(arxiv), chunk_size)]
    total = len(chunks)
    print('Chunks to process:', total)
    arxiv = list()
    count = 0
    start = time()
    for chunk in chunks:
        count = count + 1
        process_chunk(chunk)
        elapsed = time() - start
        avg = elapsed / count
        remaining = (total - count) * avg
        hours = remaining / 3600
        print(count, total - count, hours)
        #exit()
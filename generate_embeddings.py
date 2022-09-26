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


def save_data(payload):
    filename = '%s.json' % str(uuid4())
    with open('embeddings/%s' % filename, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=1)


if __name__ == '__main__':
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")
    arxiv = open_file('c:/arxiv/arxiv-metadata-oai-snapshot.json').splitlines()
    print('Articles loaded:', len(arxiv))
    #exit(0)
    errors = list()
    for article in arxiv:
        try:
            info = json.loads(article)
            #print(info['title'], info['abstract'])
            #exit(0)
            title = re.sub('\s+', ' ', info['title'].strip())
            print(title)
            abstract = re.sub('\s+', ' ', info['abstract'].strip())
            embeddings = embed([title + ' ' + abstract])
            vector = embeddings.numpy().tolist()[0]
            save_data({'title': title, 'abstract': abstract, 'embedding': vector})
            #exit(0)
        except:
            errors.append(article)
    with open('errors.json', 'w', encoding='utf-8') as outfile:
        json.dump(errors, outfile, ensure_ascii=False, sort_keys=True, indent=1)

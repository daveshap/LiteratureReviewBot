import numpy as np
import json
import os
from time import time
from qdrant_client import QdrantClient


def load_data(directory):
    files = os.listdir(directory)
    vectors = list()
    payloads = list()
    count = 0
    for file in files:
        count = count + 1
        with open('%s/%s' % (directory, file), 'r', encoding='utf-8') as infile:
            info = json.load(infile)
            vectors.append(info['embedding'])
            payloads.append({'content': info['string'], 'file': file})
        print(count, 'of', len(files), 'loaded')
    return vectors, payloads


if __name__ == '__main__':
    print('starting up...')
    vectors, payloads = load_data('data')
    print('Starting Qdrant client...')
    client = QdrantClient(host='localhost', port=6333)
    # instantiate collection
    print('Creating collection "stress_test"...')
    client.recreate_collection(
        collection_name='stress_test', 
        vector_size=512, 
        distance="Cosine")
    # upload data
    start = time()
    print('Uploading records...')
    client.upload_collection(
        collection_name='stress_test',
        vectors=vectors,
        payload=payloads,
        ids=None,
        batch_size=256)
    print('Uploaded in', time() - start, 'seconds')
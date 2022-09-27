import json
import os
from time import time
from qdrant_client import QdrantClient


def send_batch(vectors, payloads, client):
    #print('Uploading records...')
    client.upload_collection(
        collection_name='arxiv',
        vectors=vectors,
        payload=payloads,
        ids=None,
        batch_size=256)


def load_data(directory, client):
    files = os.listdir(directory)
    vectors = list()
    payloads = list()
    count = 0
    total = len(files)
    start = time()
    for file in files:
        count = count + 1
        with open('%s/%s' % (directory, file), 'r', encoding='utf-8') as infile:
            info = json.load(infile)
            vectors.append(info['embedding'])
            payloads.append({'id':info['id'], 'title':info['title'], 'abstract':info['abstract']})
        if len(vectors) >= 1000:
            send_batch(vectors, payloads, client)
            vectors = list()
            payloads = list()
            avg = (time()-start)/count
            hrs = (total - count)*avg/3600
            print(count, 'of', total, 'hours remaining:', hrs)
    send_batch(vectors, payloads, client)
    print('total hours:', (time() - start)/3600)
    


if __name__ == '__main__':
    # instantiate client
    print('Starting Qdrant client...')
    client = QdrantClient(host='localhost', port=6333)
    # instantiate collection
    print('Creating collection "arxiv"...')
    client.recreate_collection(
        collection_name='arxiv', 
        vector_size=512, 
        distance="Cosine")
    # upload data
    print('Uploading data...')
    load_data('embeddings', client)
    print('All done...')
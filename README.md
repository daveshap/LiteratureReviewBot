# Literature Review Bot

## Setup

### Docker and Qdrant

1. Download and setup Docker and/or Docker Desktop
2. Pull the Qdrant container and run it: `docker run -p 6333:6333 -v ./qdrant_storage:/qdrant/storage qdrant/qdrant`

### Download arXiv metadata from Kaggle

1. https://www.kaggle.com/datasets/Cornell-University/arxiv

Or download my processed data directly (but it is out of date)

1. https://www.kaggle.com/datasets/ltcmdrdata/arxiv-embeddings (I will not be maintaining this)

### Process data

1. Run `generate_embeddings.py` to fill up `embeddings` folder (you may need to create this folder first)
2. Fire up Qdrant if its not already running
3. Run `index_arxiv_metadata.py` to upload embeddings to Qdrant
4. Run `search_server.py` and go to http://127.0.0.1 to search for your articles
5. Download the PDFs you want from arXiv into th `PDFs` folder
6. Run `generate_literature_review.py` to create your final literature review
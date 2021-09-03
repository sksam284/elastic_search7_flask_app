import os
from elasticsearch import Elasticsearch

es = Elasticsearch(os.environ.get("DATABASE_URI"))

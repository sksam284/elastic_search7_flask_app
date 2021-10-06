import os
from elasticsearch import Elasticsearch

from dotenv import load_dotenv

load_dotenv()
hostname = os.getenv('HOST_NAME')
port = os.getenv('PORT')
es = Elasticsearch(hosts=[{"host": hostname, "port": port}], max_retries=30,
                       retry_on_timeout=True, request_timeout=30)
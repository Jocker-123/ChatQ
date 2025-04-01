from elasticsearch import Elasticsearch
import os

es = Elasticsearch(os.getenv("elasticsearch_url", "http://localhost:9200"))


def index_to_elasticsearch(docs, index_name="rag-index"):
    for i, doc in enumerate(docs):
        es.index(index=index_name, id=i, document={"content": doc.page_content})


def search_elasticsearch(query: str, index_name="rag-index"):
    res = es.search(index=index_name, query={"match": {"content": query}})
    return [hit["_source"]["content"] for hit in res["hits"]["hits"]]

# coding:utf8
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search

es = Elasticsearch()
result = es.search(index='test_index2')
print(result)
result = es.search(index='test_index2', filter_path=['hits.hits._source'])
for r in (result['hits']['hits']):
    print(r['_source'])
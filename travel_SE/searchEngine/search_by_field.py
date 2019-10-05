# coding:utf8
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search

es = Elasticsearch()
# result = es.search(index='test_index')
# print(result)
# result = es.search(index='test_index', filter_path=['hits.hits._source'])
# for r in (result['hits']['hits']):
#     print(r['_source'])

search1 = {
    'query': {
        'match_all': {},
    }
}


search2 = {
    'query': {
        'multi_match': {
            'query': '青岛',
            'type': 'best_fields',
            'fields': ['name'],
            # 'fields':['name','location'],
            'operator': 'and',
        },
    },
    "from": 0,
    "size": 50
}
count = 0
re = es.search(index='test_index', body=search2)
# print(re)
for r in (re['hits']['hits']):
    print(str(r['_score']) + r['_source']['name'])
    count += 1

print("检索到:" + str(count))

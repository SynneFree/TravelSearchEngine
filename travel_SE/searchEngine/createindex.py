# coding:utf8
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search

es = Elasticsearch()

mapping = {
    'basicInfo': {
        'properties': {
            "name": {
                "type": "text",
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            "location": {
                "type": "text",
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'province': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'city': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'district': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'abstract': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'distribution': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'rank': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'feature': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'notes': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'strategy': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer':'ik_smart',
            },
            'route': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'bestTime': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'shopping': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'traffic_info': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'ticket_info': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'openTime': {
                'type': 'text',
                'index': True,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'official_site': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'service': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'telephone': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'attention_items': {
                'type': 'text',
                'index': False,
                'analyzer': 'ik_max_word',  # 使用中文分词器
                'search_analyzer': 'ik_smart',
            },
            'map': {
                'type': 'text',
                'index': False,
            },
        }
    }
}

if es.indices.exists(index="test_index3"):
    result = es.indices.delete(index="test_index3")
    print("原索引已删除")

# result = es.create(index="test_index",doc_type="type1",body=_index_mappings,id=2)
es.indices.create(index='test_index3', ignore=400)
# 如果在创建索引时定义doc_type参数，则include_type_name=True，否则不需要定义doc_type，且include_type_name=False
result = es.indices.put_mapping(index='test_index3', doc_type='basicInfo', body=mapping, include_type_name=True)
# result = es.indices.put_mapping(index='test_index', body=mapping, include_type_name=False)
# result = es.indices.create(index="test_index", body=_index_mappings)
print("重新建立索引:"+str(result))

# Data = [
#     {
#         'name': '西湖',
#         'location': '浙江省-杭州市-西湖区',
#         'abstract': '西湖有西湖十景',
#         'province': '浙江省',
#         'city': '杭州市',
#         'district': '西湖区',
#     },
#     {
#         'name': '九寨沟',
#         'location': '四川省-阿坝藏族羌族自治州-九寨沟县',
#         'abstract': '九寨沟以翠海、叠瀑、彩林、雪峰、蓝冰、藏情合为九寨沟“六绝”，享有“童话世界”的美誉。',
#         'province': '四川省',
#         'city': '阿坝藏族羌族自治州',
#         'district': '九寨沟县',
#     },
# ]
#
# for d in Data:
#     _in = es.index(index='test_index', doc_type='basicInfo', body=d)
#     print(_in)
# success, _ = bulk(es, ACTIONS, index="test_index", raise_on_error=True)
# print('Performed %d actions' % success)

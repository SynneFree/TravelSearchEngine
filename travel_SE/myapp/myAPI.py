from django.conf import settings
import json
from elasticsearch import Elasticsearch
from xpinyin import Pinyin

es = Elasticsearch()


def load_data(dir):
    f = open(dir, encoding='utf-8')  # 打开‘.json’的json文件
    res = f.read()  # 读文件
    data = json.loads(res)
    return data


def getPinyin(CNfield):
    CNfield = CNfield.replace("市", '')
    p = Pinyin()
    ENfield = p.get_pinyin(u'' + CNfield, '')
    return ENfield


def search_by_area(area_field):
    search = {
        'query': {
            'bool': {
                'must': {
                    'match_phrase_prefix': {
                        'district': area_field
                    }
                }
            }
        },
        "from": 0,
        "size": 1000
    }
    count = 0
    # re = es.search(index='test_index2', body=search)
    re = es.search(index='test_index3', body=search)
    # print(re)
    List = []
    Scores = []
    for r in (re['hits']['hits']):
        line = r['_source']
        score = r['_score']
        List.append(line)
        Scores.append(score)
        # print(str(r['_score']) + r['_source']['name'])
        count += 1
    msg = "检索到：" + str(count) + "条记录.显示前1000条记录！"
    #print("检索到:" + str(count) + "条记录")
    return List, Scores,msg


def search_by_name_exactly(name):
    search = {
        'query': {
            'bool': {
                'must': [
                    {'match': {
                        'name': name,
                        }
                    },
                ]
            }
        },
        "from": 0,
        "size": 1
    }
    count = 0
    #re = es.search(index='test_index2', body=search)
    re = es.search(index='test_index3', body=search)
    #print(re)
    try:
        Attraction=re['hits']['hits'][0]['_source']
        # Score=re['hits']['hits'][0]['_score']
    except IndexError:
        Attraction=None
    return Attraction


def search_by_name_location(name, location):
    search = {
        'query': {
            'bool': {
                'must': [
                    {'match': {
                        'name': name,
                    }},
                    {'match': {
                        'location': location
                    }}
                ]
            }
        },
        "from": 0,
        "size": 1
    }
    count = 0
    #re = es.search(index='test_index2', body=search)
    re = es.search(index='test_index3', body=search)
    # print(re)
    List = []
    Scores = []
    for r in (re['hits']['hits']):
        line = r['_source']
        score = r['_score']
        List.append(line)
        Scores.append(score)
        # print(str(r['_score']) + r['_source']['name'])
        count += 1
    msg = "检索到：" + str(count) + "条记录.显示前1000条记录！"
    #print("检索到:" + str(count) + "条记录")
    return List, Scores


def search(search_field):
    search = {
        'query': {
            'multi_match': {
                'query': search_field,
                'type': 'most_fields',
               # 'fields': ['name^8', 'province^3','city^5','district^2', 'rank^1', 'feature^2'],
                'fields': ['name^4','province^4','city','district^2','abstract','rank','feature'],
                # 'fields':['name','location'],
                'operator': 'or',
            },
        },
        "from": 0,
        "size": 1000
    }
    count = 0
   # re = es.search(index='test_index2', body=search)
    re = es.search(index='test_index3', body=search)
    # print(re)
    List = []
    Scores = []
    for r in (re['hits']['hits']):
        line = r['_source']
        score = r['_score']
        List.append(line)
        Scores.append(score)
        # print(str(r['_score']) + r['_source']['name'])
        count += 1
    msg = "检索到：" + str(count) + "条记录.显示前1000条记录！"
    #print("检索到:" + str(count) + "条记录")
    return List, Scores, msg

def search_all():
    search = {
        'query': {
            'match_all': {},
        },
        "from": 0,
        "size": 10000,
    }
    count = 0
    #re = es.search(index='test_index2', body=search)
    re = es.search(index='test_index3', body=search)
    # print(re)
    List = []
    Scores = []
    for r in (re['hits']['hits']):
        line = r['_source']
        score = r['_score']
        List.append(line)
        Scores.append(score)
        # print(str(r['_score']) + r['_source']['name'])
        count += 1
    msg = "检索到：" + str(count) + "条记录."
    # print("检索到:" + str(count) + "条记录")
    return List, Scores, msg
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

def createindex():
    es = Elasticsearch()
    result = es.indices.create(index='news', ignore=400)
    print(result)


def deleteindex():
    es = Elasticsearch()
    result = es.indices.delete(index='news', ignore=[400,404])
    print(result)

def insert():
    es = Elasticsearch()
    data = {'title': '你好啊傻逼',
            'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
            'date':'2019-7-7'
            }
    result = es.create(index='news', doc_type='politics', id=1, body=data)
    print(result)

def insert_more():
    es = Elasticsearch()
    datas = [
        {'title': '公安部：各地校车将享最高路权', 'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml','date': '2011-12-16'},
        {'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船', 'url': 'https://news.qq.com/a/20111216/001044.htm', 'date': '2011-12-17'},
        {'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首', 'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml','date': '2011-12-18'}]
    for data in datas:
        es.index(index='news', doc_type='politics', body=data)

def update():
    es = Elasticsearch()
    data = {"doc":{
        'title': 'hello world',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2019-7-8'
    }
            }
    result = es.update(index='news', doc_type='politics', id=1,body=data, )
    print(result)

def delete():
    es = Elasticsearch()
    result = es.delete(index='news', doc_type='politics', id=1)
    print(result)

def search():
    es = Elasticsearch()
    result = es.search(index='news',filter_path=['hits.hits._*'])
    print(result)

def test():
    es = Elasticsearch()
    mapping={
        'politics':{
                'properties':{
                    'title':{
                        'type':'text',
                        'analyzer': 'ik_max_word',  # 使用中文分词器
                        'search_analyzer': 'ik_max_word',
                    }
                }
        }
    }
    # mapping = {'properties':
    #                {'title':
    #                     {'type': 'text',
    #                      'analyzer': 'ik_max_word',#使用中文分词器
    #                      'search_analyzer': 'ik_max_word'
    #                      }
    #                 }
    #            }
    #es.indices.delete(index='news', ignore=[400, 404])
    #es.indices.create(index='news', ignore=400)
    result = es.indices.put_mapping(index='news', doc_type='politics',body=mapping,include_type_name=True)
    print(result)

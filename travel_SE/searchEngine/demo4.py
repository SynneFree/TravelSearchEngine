from elasticsearch import Elasticsearch

es=Elasticsearch(['localhost:9200'])
body={
    'title':'day day up',
    'number': 10,
    'time':'2019-7-7',
}
es.index(index='index1',doc_type='type1',body=body,id=123)
es.get(index='index1',doc_type='type1',id=123)

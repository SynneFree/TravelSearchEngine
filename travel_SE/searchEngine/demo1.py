#coding:utf8
from elasticsearch import Elasticsearch
es = Elasticsearch()

mappings = {
            "mappings": {
                    "properties": {
                        "id": {
                            "type": "long",
                            "index": "false"
                        },
                        "serial": {
                            "type": "keyword",  # keyword不会进行分词,text会分词
                            "index": "false"  # 不建索引
                        },
                        #tags可以存json格式，访问tags.content
                        "tags": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "keyword", "index": True},
                                "dominant_color_name": {"type": "keyword", "index": True},
                                "skill": {"type": "keyword", "index": True},
                            }
                        },
                        "hasTag": {
                            "type": "long",
                            "index": True
                        },
                        "status": {
                            "type": "long",
                            "index": True
                        },
                        "createTime": {
                            "type": "date",
                        },
                        "updateTime": {
                            "type": "date",
                        }
                    }
                }
        }

res = es.indices.create(index = 'index_test',body =mappings)
# coding=utf-8

# 尝试搜索Elasticsearch
from elasticsearch import Elasticsearch
import TaxPolicyCrawlerScrapy.util.Constants as Constants


def search_by_key(key):
    es = Elasticsearch()
    query = {"query": {"match": {"content": key}}}
    ret = es.search(index=Constants.es_index_name,
                    doc_type=Constants.es_type_explain + ',' + Constants.es_type_law,
                    body=query)
    print(str(ret))

# 测试搜索
search_by_key('2017')

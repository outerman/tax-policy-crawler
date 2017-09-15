# coding=utf-8

# 尝试搜索Elasticsearch
from elasticsearch import Elasticsearch
import TaxPolicyCrawlerScrapy.util.Constants as Constants


# 使用key在content里搜索
def search_by_key(key):
    es = Elasticsearch()
    query = {"query": {"match": {"content": key}}}
    ret = es.search(index=Constants.es_index_name,
                    doc_type=Constants.es_type_explain + ',' + Constants.es_type_law,
                    body=query)
    print(str(ret))


# 删除索引
def delete_index(index_name):
    es = Elasticsearch()
    es.indices.delete(index=index_name)
    print("delete index '" + index_name + "' succeed")


# 测试搜索
# search_by_key('2017')
delete_index(Constants.es_index_name)

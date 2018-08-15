# coding=utf-8

# Elasticsearch相关接口
from elasticsearch import Elasticsearch
import TaxPolicyCrawlerScrapy.util.Constants as Constants
from TaxPolicyCrawlerScrapy import settings

es = Elasticsearch(hosts=[{"host": settings.ES_HOST, "port": 9200}])


# 使用key在content里搜索
def search_by_key(key):
    query = {"query": {"match": {"content": key}}}
    ret = es.search(index=Constants.es_index_name,
                    # doc_type=Constants.es_type_explain + ',' + Constants.es_type_law,
                    # doc_type=Constants.DocTypeChinaTax.doc_type + ',' + Constants.DocTypeShui5.doc_type,
                    doc_type=Constants.default_doc_type,
                    body=query)
    print(str(ret))
    return ret


# 根据url搜索，精确查找
def exists_by_url(url):
    query = {"query": {"term": {"url": url}}}
    try:
        ret = es.search(index=Constants.es_index_name,
                        # doc_type=Constants.es_type_explain + ',' + Constants.es_type_law,
                        # doc_type=Constants.DocTypeChinaTax.doc_type + ',' + Constants.DocTypeShui5.doc_type,
                        doc_type=Constants.default_doc_type,
                        body=query)
        # print(str(ret))
        return ret.get('hits').get('total') > 0
    except Exception as ex:
        print(ex)
    return False


# 根据md5搜索，精确查找
def exists_by_md5(md5):
    query = {"query": {"term": {"md5": md5}}}
    try:
        ret = es.search(index=Constants.es_index_name,
                        # doc_type=Constants.es_type_explain + ',' + Constants.es_type_law,
                        # doc_type=Constants.DocTypeChinaTax.doc_type + ',' + Constants.DocTypeShui5.doc_type,
                        doc_type=Constants.default_doc_type,
                        body=query)
        # print(str(ret))
        return ret.get('hits').get('total') > 0
    except Exception as ex:
        print(ex)
    return False


# 删除索引
def delete_index(index_name):
    es.indices.delete(index=index_name)
    print("delete index '" + index_name + "' succeed")


# 查询索引
def get_index(index_name):
    return es.indices.get(index=index_name)


# 创建索引（# TODO：暂时没有支持setting）
def create_index(index_name, mapping=None, setting=None):
    es.indices.create(index_name, body={'mappings': mapping})


# 查询索引是否存在
def exists_index(index_name):
    return es.indices.exists(index=index_name)


# 保存爬取的数据
def save(index, doc_type, body):
    return es.index(index=index, doc_type=Constants.default_doc_type, body=body)

# 测试搜索
# create_index(Constants.es_index_name, mapping=Constants.default_es_mapping)# es_mapping)
# search_by_key('2017')
# delete_index(Constants.es_index_name)
# ElasticSearchPipeline.check_elastic_indices()
# print(exists_by_url("../../n810341/n810760/c1152203/content.html"))

# create_index(Constants.es_index_name, {
#     "policy_explain": {
#         "properties": {
#             "content": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "date": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "hash_md5": {
#                 "type": "string",
#                 "index": "not_analyzed",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "policyType": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "publisher": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "source": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "timestamp": {
#                 "type": "float"
#             },
#             "title": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             },
#             "url": {
#                 "type": "string",
#                 "index": "not_analyzed",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 }
#             }
#         }
#     }
# })


# print(get_index(Constants.es_index_name))

# print(exists_index(Constants.es_index_name))

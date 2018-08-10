# coding=utf-8

# 常量类
# 基本数据设定

es_host = '172.16.20.43'
proxy_host = '172.16.20.43'

# 所有政策法规的爬取数据，都放到一个索引下
es_index_name = 'tax_policy'
# es_type_law = 'policy_law'
# es_type_explain = 'policy_explain'

# 由于ElasticSearch在6.X以后，只支持single-type，以及后续会逐步把mapping-types去掉，使用默认的doc_type
# https://www.elastic.co/guide/en/elasticsearch/reference/6.0/removal-of-types.html
default_doc_type = "doc"

# 目前所有的税收政策，都放在同一个index里
default_es_mapping = {
    "doc": {            # 由于single-type，这里固定为"doc"，与default_doc_type保持一致
        "properties": {
            "doc_type": {
                "type": "keyword"
            },
            "content": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "date": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "hash_md5": {
                "type": "keyword"
                # "type": "string",
                # "index": "not_analyzed",  # here
                # "fields": {
                #     "keyword": {
                #         "type": "keyword",
                #         "ignore_above": 256
                #     }
                # }
            },
            "policyType": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "publisher": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "source": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "timestamp": {
                "type": "float"
            },
            "title": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "url": {
                # "type": "string",
                # "index": "not_analyzed",  # here
                # "fields": {
                #     "keyword": {
                #         "type": "keyword",
                #         "ignore_above": 256
                #     }
                # }
                "type": "keyword"
            }
        }
    }
}


# 不同来源的数据，放到不同的doc_type下; 统一来源的不同分类，使用policy_type来区分
# 1）国税总局
# doc_type_chinatax = {
#     'doc_Type': 'chinaTax',
#     'source_name': '国税总局',
#     'policy_types': {'policy_law': '税收法规库', 'policy_explain': '政策解读'}
# }
class DocTypeChinaTax:
    doc_type = 'chinaTax'
    source_name = '国税总局'
    policy_types = {
        'policy_law': '税收法规库',
        'policy_explain': '政策解读'
    }


# 2）税屋
# doc_type_shui5 = {
#     'doc_Type': 'shui5',
#     'source_name': '税屋',
#     'policy_types': {'policy_explain': '法规解读'}
# }
class DocTypeShui5:
    doc_type = 'shui5'
    source_name = '税屋'
    policy_types = {
        'policy_explain': '法规解读'
    }
    # es_mapping = {
    #     "properties": {
    #         "content": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             },
    #             "analyzer": "ik_max_word",
    #             "search_analyzer": "ik_max_word"
    #         },
    #         "date": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             }
    #         },
    #         "hash_md5": {
    #             "type": "keyword"
    #         },
    #         "policyType": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             },
    #             "analyzer": "ik_max_word",
    #             "search_analyzer": "ik_max_word"
    #         },
    #         "publisher": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             },
    #             "analyzer": "ik_max_word",
    #             "search_analyzer": "ik_max_word"
    #         },
    #         "source": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             },
    #             "analyzer": "ik_max_word",
    #             "search_analyzer": "ik_max_word"
    #         },
    #         "subtitle": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             },
    #             "analyzer": "ik_max_word",
    #             "search_analyzer": "ik_max_word"
    #         },
    #         "timestamp": {
    #             "type": "float"
    #         },
    #         "title": {
    #             "type": "text",
    #             "fields": {
    #                 "keyword": {
    #                     "type": "keyword",
    #                     "ignore_above": 256
    #                 }
    #             },
    #             "analyzer": "ik_max_word",
    #             "search_analyzer": "ik_max_word"
    #         },
    #         "url": {
    #             "type": "keyword"
    #         }
    #     }
    # }

# 配置所有的doc_type，用于初始化es中的相关结构。
# TODO：也许有更好的方式
# all_doc_types = [DocTypeChinaTax(), DocTypeShui5()]

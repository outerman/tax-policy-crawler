# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaxpolicycrawlerscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PolicyItem(scrapy.Item):
    title = scrapy.Field()  # 标题: 国家税务总局关于卷烟消费税计税价格核定管理有关问题的公告
    subtitle = scrapy.Field()  # 副标题：国家税务总局公告2017年第32号
    date = scrapy.Field()  # 发文日期
    content = scrapy.Field()  # 正文内容
    publisher = scrapy.Field()  # 发文部门
    url = scrapy.Field()  # 链接地址
    md5 = scrapy.Field()  # md5判断是否重复


class PolicySource(scrapy.Item):
    source = scrapy.Field()  # 政策来源: 国税总局、各省市区税务局
    policyType = scrapy.Field()  # 政策类型：税收法规库、政策解读、与外国的税收条约
    taxLevel = scrapy.Field()  # 税种：国税、地税


# 在ElasticSearch中index的mapping，重点在定义几个not_analyzed字段
# 使用elasticsearch-analysis-ik分词插件，增加分词相关的配置analyzer和search_analyzer
# mappings = {
#     "policy_explain": {
#         "properties": {
#             "content": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
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
#                 "type": "keyword"
#                 # "type": "string",
#                 # "index": "not_analyzed",  # here
#                 # "fields": {
#                 #     "keyword": {
#                 #         "type": "keyword",
#                 #         "ignore_above": 256
#                 #     }
#                 # }
#             },
#             "policyType": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "publisher": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "source": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
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
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "url": {
#                 # "type": "string",
#                 # "index": "not_analyzed",  # here
#                 # "fields": {
#                 #     "keyword": {
#                 #         "type": "keyword",
#                 #         "ignore_above": 256
#                 #     }
#                 # }
#                 "type": "keyword"
#             }
#         }
#     },
#     "policy_law": {
#         "properties": {
#             "content": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
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
#                 "type": "keyword"
#             },
#             "policyType": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "publisher": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "source": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "subtitle": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword",
#                         "ignore_above": 256
#                     }
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
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
#                 },
#                 "analyzer": "ik_max_word",
#                 "search_analyzer": "ik_max_word"
#             },
#             "url": {
#                 "type": "keyword"
#             }
#         }
#     }
# }

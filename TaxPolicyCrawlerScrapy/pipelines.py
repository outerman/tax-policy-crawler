# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from TaxPolicyCrawlerScrapy.items import PolicySource
from elasticsearch import Elasticsearch
import hashlib
import time
import json


# 把两个对象，转化为es可保存的对象，并为一个
def get_es_body(policy_source, item, hash_md5, timestamp):
    _dict = policy_source.__dict__
    _dict.update(item.__dict__)
    _dict['hash_md5'] = hash_md5
    _dict['timestamp'] = timestamp
    return _dict


class TaxpolicycrawlerscrapyPipeline(object):
    es_index_name = 'tax_policy'
    es_type_law = 'policy_law'
    es_type_explain = 'policy_explain'

    def __init__(self) -> None:
        super().__init__()
        self.es = Elasticsearch()

    def process_item(self, item, spider):
        if not item or (not item.get('title') and not item.get('content')):
            print('Get an EMPTY item:' + str(item))
            return item
        # 区分各个spider来的，使用不同的PolicySource
        if spider.name == 'TaxPolicyExplainCrawler':
            policy_source = PolicySource()
            policy_source['source'] = '国税总局'
            policy_source['policyType'] = '政策解读'
            doc_type = self.es_type_explain
        elif spider.name == 'TaxPolicyCrawler':
            policy_source = PolicySource()
            policy_source['source'] = '国税总局'
            policy_source['policyType'] = '税收法规库'
            doc_type = self.es_type_law
        else:
            return item

        # Md5，及排重
        hash_md5 = hashlib.md5(item.get('content').encode('utf-8')).hexdigest()

        # 插入前的时间戳等字段
        timestamp = time.time()

        # 拼装成最终存储结构
        body_dict = json.dumps(get_es_body(policy_source, item, hash_md5, timestamp)['_values'], ensure_ascii=False)

        # 存储——Elasticsearch
        self.es.index(index=self.es_index_name, doc_type=doc_type, body=body_dict)

        return item

# -*- coding: utf-8 -*-

# 在pipelines保存前的公共数据转换
import hashlib
import time
from TaxPolicyCrawlerScrapy.items import PolicySource
from TaxPolicyCrawlerScrapy.util import Constants


def get_es_body(policy_source, item, hash_md5, timestamp):
    _dict = dict(policy_source.__dict__['_values'])
    _dict.update(item.__dict__['_values'])
    _dict['hash_md5'] = hash_md5
    _dict['timestamp'] = timestamp
    return _dict


def convert_item(item, spider):
    if not item or (not item.get('title') and not item.get('content')):
        print('Get an EMPTY item:' + str(item))
        return None
    # 区分各个spider来的，使用不同的PolicySource
    if spider.name == 'TaxPolicyExplainCrawler':
        policy_source = PolicySource()
        policy_source['source'] = '国税总局'
        policy_source['policyType'] = '政策解读'
        doc_type = Constants.es_type_explain
    elif spider.name == 'TaxPolicyCrawler':
        policy_source = PolicySource()
        policy_source['source'] = '国税总局'
        policy_source['policyType'] = '税收法规库'
        doc_type = Constants.es_type_law
    else:
        return None

    # Md5，及排重
    hash_md5 = hashlib.md5(item.get('content').encode('utf-8')).hexdigest()

    # 插入前的时间戳等字段
    timestamp = time.time()

    # 拼装成最终存储结构
    return doc_type, get_es_body(policy_source, item, hash_md5, timestamp)

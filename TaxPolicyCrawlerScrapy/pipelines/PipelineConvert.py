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

    if not spider.doc_type or not spider.policy_source:
        print("************* no doc_type or policy_source ****************")
        return None

    # Md5，及排重
    hash_md5 = hashlib.md5(item.get('content').encode('utf-8')).hexdigest()

    # 插入前的时间戳等字段
    timestamp = time.time()

    # 拼装成最终存储结构
    return spider.doc_type, get_es_body(spider.policy_source, item, hash_md5, timestamp)

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from elasticsearch import Elasticsearch

import TaxPolicyCrawlerScrapy.util.Constants as Constants
# 把两个对象，转化为es可保存的对象，并为一个
from TaxPolicyCrawlerScrapy.pipelines import PipelineConvert


class ElasticSearchPipeline(object):

    def __init__(self) -> None:
        super().__init__()
        self.es = Elasticsearch()

    def process_item(self, item, spider):
        doc_type, body_dict = PipelineConvert.convert_item(item, spider)

        # 拼装成最终存储结构
        body_dict = json.dumps(body_dict, ensure_ascii=False)
        # 存储——Elasticsearch
        self.es.index(index=Constants.es_index_name, doc_type=doc_type, body=body_dict)
        return item

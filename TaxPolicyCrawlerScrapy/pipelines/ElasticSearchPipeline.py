# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import TaxPolicyCrawlerScrapy.util.Constants as Constants
# 把两个对象，转化为es可保存的对象，并为一个
from TaxPolicyCrawlerScrapy import items
from TaxPolicyCrawlerScrapy.pipelines import PipelineConvert
from TaxPolicyCrawlerScrapy.util import ElasticSearchUtil


# 检查ElasticSearch的相关索引是否已经创建，如果没有则创建之（因为不能单纯使用默认的索引）
def check_elastic_indices():
    if not ElasticSearchUtil.exists_index(Constants.es_index_name):
        ElasticSearchUtil.create_index(Constants.es_index_name, mapping=items.mappings)
        # TODO: 自定义中文分词器，以提高中文搜索效果，例如elasticsearch-analysis-ik
        # 看笔记，1）在ElasticSearch的docker镜像里，安装插件  2）在创建索引时候，增加analyzer和search_analyzer的配置


class ElasticSearchPipeline(object):

    def __init__(self) -> None:
        super().__init__()
        check_elastic_indices()

    def process_item(self, item, spider):
        doc_type, body_dict = PipelineConvert.convert_item(item, spider)

        # 拼装成最终存储结构
        body_dict = json.dumps(body_dict, ensure_ascii=False)
        # 存储——Elasticsearch
        ElasticSearchUtil.save(index=Constants.es_index_name, doc_type=doc_type, body=body_dict)
        return item

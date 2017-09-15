# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import TaxPolicyCrawlerScrapy.util.Constants as Constants


# 把两个对象，转化为es可保存的对象，并为一个
from TaxPolicyCrawlerScrapy.pipelines import PipelineConvert
from TaxPolicyCrawlerScrapy.util import ExcelUtil


class ExcelPipeline(object):
    def process_item(self, item, spider):
            doc_type, body_dict = PipelineConvert.convert_item(item, spider)
            ExcelUtil.save_to_excel(Constants.es_index_name, doc_type=doc_type, item_list=[body_dict])

            return item

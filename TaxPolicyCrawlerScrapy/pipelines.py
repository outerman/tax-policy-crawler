# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from TaxPolicyCrawlerScrapy.items import PolicySource


class TaxpolicycrawlerscrapyPipeline(object):
    def process_item(self, item, spider):
        if not item or (not item.get('title') and not item.get('content')):
            print('Get an EMPTY item:' + str(item))
            return item
        # 区分各个spider来的，使用不同的PolicySource
        if spider.name == 'TaxPolicyExplainCrawler':
            policy_source = PolicySource('国税总局', '政策解读', '')
        elif spider.name == 'TaxPolicyCrawler':
            policy_source = PolicySource('国税总局', '税收法规库', '')


        # TODO: 多种存储
        # TODO: Md5，及排重
        return item

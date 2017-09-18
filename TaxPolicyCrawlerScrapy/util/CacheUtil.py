# coding=utf-8

# 缓存工具类，用于判断一个页面是否已经被爬取过


# 根据url检查是否已经爬取过
from TaxPolicyCrawlerScrapy.util import ElasticSearchUtil


def is_url_crawled(url):
    if ElasticSearchUtil.exists_by_url(url):
        return True
    return False


# 根据md5检查是否已经爬取过
def is_md5_crawled(md5):
    if ElasticSearchUtil.exists_by_md5(md5):
        return True
    return False

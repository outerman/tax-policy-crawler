# # 简单的跑一个Crawler，使用当前配置
# from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'TaxPolicyCrawler']) # 'TaxPolicyCrawler' #'TaxPolicyExplainCrawler'


# 使用CrawlerProcess，"并行"跑一组Crawler，使用指定配置
from scrapy.crawler import CrawlerProcess
from TaxPolicyCrawlerScrapy.spiders.chinatax.TaxPolicyCrawler import TaxPolicyCrawler
from TaxPolicyCrawlerScrapy.spiders.chinatax.TaxPolicyExplainCrawler import TaxPolicyExplainCrawler
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(TaxPolicyCrawler)
process.crawl(TaxPolicyExplainCrawler)
process.start()


# # 使用CrawlerRunner，"并行"跑一组Crawler，使用指定配置
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from TaxPolicyCrawlerScrapy.spiders.chinatax.TaxPolicyCrawler import TaxPolicyCrawler
# from TaxPolicyCrawlerScrapy.spiders.chinatax.TaxPolicyExplainCrawler import TaxPolicyExplainCrawler
# from scrapy.utils.project import get_project_settings
#
# configure_logging()
# runner = CrawlerRunner(get_project_settings())
# runner.crawl(TaxPolicyCrawler)
# runner.crawl(TaxPolicyExplainCrawler)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
#
# # the script will block here until all crawling jobs are finished
# reactor.run()


# # 使用CrawlerRunner，"串行"跑一组Crawler，使用指定配置
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from TaxPolicyCrawlerScrapy.spiders.chinatax.TaxPolicyCrawler import TaxPolicyCrawler
# from TaxPolicyCrawlerScrapy.spiders.chinatax.TaxPolicyExplainCrawler import TaxPolicyExplainCrawler
# from scrapy.utils.log import configure_logging
#
# configure_logging()
# runner = CrawlerRunner()
#
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(TaxPolicyCrawler)
#     yield runner.crawl(TaxPolicyExplainCrawler)
#     reactor.stop()
#
# crawl()
# reactor.run() # the script will block here until the last crawl call is finished

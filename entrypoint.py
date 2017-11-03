from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'TaxPolicyExplainCrawler'])  # 'TaxPolicyCrawler' #'TaxPolicyExplainCrawler'
execute(['scrapy', 'crawl', 'TaxPolicyCrawler'])



# from twisted.internet import reactor, defer
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from TaxPolicyCrawlerScrapy.spiders.TaxPolicyCrawler import TaxPolicyCrawler
# from TaxPolicyCrawlerScrapy.spiders.TaxPolicyExplainCrawler import TaxPolicyExplainCrawler

# configure_logging()
# runner = CrawlerRunner()
# runner.crawl(TaxPolicyCrawler)
# runner.crawl(TaxPolicyExplainCrawler)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
#
# # the script will block here until all crawling jobs are finished
# reactor.run()




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
# reactor.run()






# from scrapy.crawler import CrawlerProcess
# process = CrawlerProcess()
# process.crawl(TaxPolicyCrawler)
# process.crawl(TaxPolicyExplainCrawler)
# process.start()
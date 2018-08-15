# coding=utf-8

# 下载器中间件，主要增加动态IP代理
import base64
import TaxPolicyCrawlerScrapy.util.ProxyMgr as ProxyMgr


class ProxyDownloaderMiddleware(object):
    # 这个中间件，只需要确定proxy位置，放到meta['proxy']里，然后通过配置，由scrapy自带的downloadermiddleware.httpproxy来生效
    def process_request(self, request, spider):
        proxy = ProxyMgr.get_proxy()
        if proxy is None:
            print("**************ProxyMiddleware no poxy************")
        elif proxy.get('user_pass') is not None:
            request.meta['proxy'] = proxy['http']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print("**************ProxyMiddleware use proxy with pass************" + proxy['http'])
        else:
            print("**************ProxyMiddleware use proxy without pass************" + proxy['http'])
            request.meta['proxy'] = proxy['http']

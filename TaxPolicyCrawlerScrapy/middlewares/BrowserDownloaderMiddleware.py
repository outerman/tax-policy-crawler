# coding=utf-8

import time
from scrapy.http import HtmlResponse


# 下载器中间件，使用headless chrome来执行下载，破解js动态脚本等需要浏览器解析执行才能实现界面展现的"反爬虫"手段
# 需要同时支持使用&不使用 headless chrome的情况（settings里的downloadermiddleware.httpproxy中间件不能去掉）
class BrowserDownloaderMiddleware(object):

    def process_request(self, request, spider):
        if hasattr(spider, 'is_use_browser') and spider.is_use_browser:
            spider.browser.get(request.url)  # 用谷歌浏览器访问url
            # 使用browser，由于还没有proxy，多等几秒
            time.sleep(3)
            # TODO 如果有proxy，怎么处理？这个中间件的位置，应该在添加代理中间件之后，scrapy的框架下载中间件之前
            print('headless browser access：{0}'.format(request.url))  # 打印访问网址
            # 设置响应信息，由浏览器响应信息返回
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf-8',
                                request=request)


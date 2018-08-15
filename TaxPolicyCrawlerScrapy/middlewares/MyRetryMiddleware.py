import logging
import random

import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from TaxPolicyCrawlerScrapy.util import ProxyMgr


class MyRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def delete_proxy(self, proxy):
        if proxy:
            # delete proxy from proxies pool
            ProxyMgr.delete_proxy(proxy)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            time.sleep(random.randint(3, 5))
            self.logger.warning('连接异常, 进行重试...')

            return self._retry(request, exception, spider)
# coding=utf-8

# 请求工具类
import random
import requests
import time
import src.ProxyMgr as proxy


class RequestUtil:
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.session = None

    def post(self, url, param_data=None, num_retries=6, timeout=10):
        # 带重试策略的请求, 默认6次
        try:
            return self.session.post(url, param_data, timeout=timeout)
        except Exception as ex:
            print(u'post获取网页出错，1s后将获取倒数第：%d次: %s' % (num_retries, str(ex)))
            time.sleep(1)
            if num_retries > 0:
                num_retries -= 1
                return self.post(url, param_data, num_retries, timeout=timeout)
            else:
                # 重试失败后，删除该代理
                proxy.delete_proxy(self.session.proxies)
                raise  # 从新抛出该异常

    def get(self, url, num_retries=6, timeout=10):
        # 带重试策略的请求, 默认6次
        try:
            return self.session.get(url, timeout=timeout)
        except Exception as ex:
            print(u'get获取网页出错，1s后将获取倒数第：%d次: %s' % (num_retries, str(ex)))
            time.sleep(1)
            if num_retries > 0:
                num_retries -= 1
                return self.get(url, num_retries, timeout=timeout)
            else:
                # 重试失败后，删除该代理
                proxy.delete_proxy(self.session.proxies)
                raise   # 从新抛出该异常

    # 刷新主页，获取session（包含cookies信息, ua信息）
    def init_session(self, url, useProxy=True):
        session = requests.Session()
        self.session = session
        # 设置代理
        if useProxy:
            self.session.proxies = proxy.get_proxy()
        # 设置伪造的UA
        ua_headers = {'User-Agent': random.choice(self.user_agent_list)}
        self.session.headers.update(ua_headers)
        # 刷新主页，获取cookies
        self.get(url)

        return self


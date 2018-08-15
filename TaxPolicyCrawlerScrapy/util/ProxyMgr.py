# coding=utf-8

# 代理管理类，调用外部的proxy_pool服务，来管理代理

import requests
import re
import TaxPolicyCrawlerScrapy.settings as setting

# 简单的 ip:port 的正则表达式
from TaxPolicyCrawlerScrapy import settings
from TaxPolicyCrawlerScrapy.util import Constants

ip_reg_str = "^([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,6}$"


def get_proxy():
    if not setting.USE_PROXY:
        return None

    ip_address = requests.get("http://" + settings.PROXY_HOST + ":5000/get/").text
    if not ip_address:
        return {}

    pattern = re.compile(ip_reg_str)
    match = pattern.match(ip_address)
    if not match:
        return {}

    proxy = match.group()
    print("use proxy:" + proxy)
    return {"http": "http://{}".format(proxy)}


def delete_proxy(proxy):
    requests.get("http://" + settings.PROXY_HOST + ":5000/delete/?proxy={}".format(proxy))


# print(get_proxy())

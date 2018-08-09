# coding=utf-8
import threading
import scrapy
from bs4 import BeautifulSoup
from TaxPolicyCrawlerScrapy.items import PolicyItem, PolicySource
from TaxPolicyCrawlerScrapy.util import CacheUtil, Constants

# 国税总局，税收法规库的抓取
# http://hd.chinatax.gov.cn/guoshui/main.jsp
# 2017.9.8 共3531项查询结果236页
base_url = 'http://hd.chinatax.gov.cn/guoshui'


class TaxPolicyCrawler(scrapy.Spider):
    # 框架使用的属性，用于分类存储
    policy_source = PolicySource()
    doc_type = Constants.DocTypeChinaTax.doc_type
    policy_source['source'] = Constants.DocTypeChinaTax.source_name    # '国税总局'
    policy_source['policyType'] = Constants.DocTypeChinaTax.policy_types['policy_law']  # '税收法规库'

    # spider的名称，与setting配置里的一致；必须要有name属性，否则scrapy不做识别
    name = "TaxPolicyCrawler"

    # 当前爬虫，request使用的headers
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # self.name = self.__class__.name  # spider必须要有name属性，否则scrapy不做识别
    #     self.policy_source['source'] = '国税总局'
    #     self.policy_source['policyType'] = '税收法规库'

    # 蜘蛛打开的时执行
    def open_spider(self, spider):
        pass

    # 蜘蛛关闭时执行
    def close_spider(self, spider):
        pass

    # 可访问核心组件比如配置和信号，并注册钩子函数到Scrapy中
    # def from_crawler(cls, crawler, **kwargs):
    # # 需要返回一个Crawler
    #     pass

    def start_requests(self):
        yield scrapy.Request(base_url + '/main.jsp', method='GET', headers=self.headers, callback=self.parse_main)

    # 刷新了主页后的解析：获取了cookies，下一步抓取分页总数summary
    def parse_main(self, response):
        if not response:
            return

        print('获取分页信息：')
        form_data = 'articleField01=' \
                    '&articleField03=' \
                    '&articleField04=' \
                    '&articleField05=' \
                    '&articleField06=' \
                    '&articleField07_d=' \
                    '&articleField07_s=' \
                    '&articleField08=' \
                    '&articleField09=' \
                    '&articleField10=' \
                    '&articleField11=' \
                    '&articleField12=' \
                    '&articleField13=' \
                    '&articleField14=' \
                    '&articleField18=%E5%90%A6' \
                    '&articleRole=0000000' \
                    '&channelId=' \
                    '&intvalue=-1' \
                    '&intvalue1=4' \
                    '&rtoken=fgk' \
                    '&shuizhong=%E6%80%BB%E5%B1%80%E6%B3%95%E8%A7%84'

        yield scrapy.Request(base_url + '/action/InitNewArticle.do',
                             method='POST',
                             body=form_data,
                             headers=self.headers,
                             callback=self.parse_summary)

    # 刷新列表首页后的解析：获取分页数，然后根据分页抓取
    def parse_summary(self, response):
        page_count = parse_item_summary(response.body)
        print('page_count:' + str(page_count))

        if not page_count or page_count <= 0:
            print('获取税收法规库信息失败，可能被禁止权限了。。。')
            return

        for index in range(page_count):
            form_data = 'articleField01=' \
                        '&articleField03=' \
                        '&articleField04=' \
                        '&articleField05=' \
                        '&articleField06=' \
                        '&articleField07_d=' \
                        '&articleField07_s=' \
                        '&articleField08=' \
                        '&articleField09=' \
                        '&articleField10=' \
                        '&articleField11=' \
                        '&articleField12=' \
                        '&articleField13=' \
                        '&articleField14=' \
                        '&articleField18=%E5%90%A6' \
                        '&articleRole=0000000' \
                        '&intvalue=-1' \
                        '&intvalue1=4' \
                        '&intFlag=0' \
                        '&cPage=' + str(index + 1) + '' \
                        '&rtoken=fgk' \
                        '&shuizhong=%E6%80%BB%E5%B1%80%E6%B3%95%E8%A7%84'
            yield scrapy.Request(base_url + '/action/InitNewArticle.do',
                                 method='POST',
                                 headers=self.headers,
                                 body=form_data,
                                 callback=self.parse_list)

    # 刷新分页的列表后的解析：获取每项政策详情链接，然后抓取详情
    def parse_list(self, response):
        item_list = parse_item_list(response.body)

        if not item_list:
            return

        for item in item_list:
            url = item.get('url')
            print(threading.current_thread().name + ',抓取网页：' + url)
            if url is None:
                continue

            if CacheUtil.is_url_crawled(url):
                print('url：' + url + ' 已经抓取过，不重复抓取')
                continue

            full_url = url      # base_url + url[2:]
            yield scrapy.Request(full_url,
                                 method='GET',
                                 headers=self.headers,
                                 meta={'policy_item': item},
                                 priority=1)        # 抓取详情的request的优先级，高于抓取列表的，试图尽量一页一页的抓取

    # 默认解析器，在Request没有填写callback时调用：解析最后的详情，并发送到items及pipelines
    def parse(self, response):
        yield get_policy_detail(response.body, response.meta['policy_item'])


# 解析分页总数
def parse_item_summary(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    all_table_tags = soup.find_all('table')

    if not all_table_tags:
        return

    for tableTag in all_table_tags:
        tr_tags = tableTag.find_all('tr')

        if not tr_tags:
            continue

        page_size = get_page_size(tr_tags[0])  # 从第一个tr里分析页数
        if page_size >= 0:
            return page_size
    return 0


# 获取政策列表（分页）
def get_page_size(tr_tag):
    td_str = get_text_in_tr(tr_tag, 0)  # 获取第一个节点的字符串
    start = td_str.find('页 1/')

    if start < 0:
        return start

    start += len('页 1/')
    end = td_str.find(' ', start)

    return int(td_str[start: end])


# 解析每页里的详情标题、链接
def parse_item_list(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    target_table = soup.find('table', {'cellspacing': "1"})

    if not target_table:
        return []

    tr_tags = target_table.find_all('tr')

    if not tr_tags:
        return []

    policy_list = []
    for tr in tr_tags:
        all_tds = tr.find_all('td')
        if len(all_tds) <= 0:
            continue

        a_tag = all_tds[0].find('a')
        if not a_tag:
            continue

        policy_list.append(PolicyItem(title=a_tag.text,
                                      url=base_url + a_tag.attrs['href'][2:],
                                      subtitle=all_tds[2].text,
                                      date=all_tds[1].text))

    return policy_list


# 根据链接爬取详情
def get_policy_detail(page_text, item):
    if not item or not item.get('url'):
        return

    # 获取详情页
    soup = BeautifulSoup(page_text, "lxml")
    all_table_tags = soup.find_all('tbody')
    if not all_table_tags or len(all_table_tags) < 3:
        return

    # 找到td
    target_td = all_table_tags[2].find('td')

    # 所有内容的<p>节
    item['content'] = target_td.text
    # content_p_list = target_td.find_all('p')
    # item['content'] = ''
    # for p in content_p_list:
    #     item['content'] += '\n<br>\n'
    #     item['content'] += p.text

    # 签名的<p>节
    publisher_p_list = target_td.find_all('p', style=True)
    item['publisher'] = ''
    for p in publisher_p_list:
        item['publisher'] += '\n<br>\n'
        item['publisher'] += p.text

    return item


# 从table的tr节里，获取文案
def get_text_in_tr(tr_tag, index):
    all_tds = tr_tag.find_all('td')
    if len(all_tds) <= index:
        return ''

    td_str = all_tds[index]

    return td_str.text


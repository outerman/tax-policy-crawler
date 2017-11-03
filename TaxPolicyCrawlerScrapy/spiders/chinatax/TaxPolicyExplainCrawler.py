# coding=utf-8
import threading
import scrapy
from bs4 import BeautifulSoup
from TaxPolicyCrawlerScrapy.items import PolicyItem, PolicySource
from TaxPolicyCrawlerScrapy.util import CacheUtil, Constants

# 国税总局，政策解读
# http://www.chinatax.gov.cn/n810341/n810760/index.html
# 2017.9.8 约22页 * 25行每页 = 550行
base_url = 'http://www.chinatax.gov.cn/n810341/n810760/index.html'


class TaxPolicyExplainCrawler(scrapy.Spider):
    # 框架使用的属性
    policy_source = PolicySource()
    doc_type = Constants.es_type_explain
    name = "TaxPolicyExplainCrawler"  # spider必须要有name属性，否则scrapy不做识别
    policy_source['source'] = '国税总局'
    policy_source['policyType'] = '政策解读'
    # 当前爬虫，request使用的headers
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.name = self.__class__.name  # spider必须要有name属性，否则scrapy不做识别
    #     self.policy_source['source'] = '国税总局'
    #     self.policy_source['policyType'] = '政策解读'

    def start_requests(self):
        yield scrapy.Request(base_url, method='GET', headers=self.headers, callback=self.parse_summary)

    # 刷新列表首页后的解析：获取分页数，然后根据分页抓取
    def parse_summary(self, response):
        page_count = parse_item_summary(response.body)
        print('page_count:' + str(page_count))

        if not page_count or page_count <= 0:
            print('获取政策解读信息失败，可能被禁止权限了。。。')
            return

        # 第一页可直接解析
        self.parse_list(response.body)

        # 爬取剩余的页
        for page_index in range(1, page_count):
            url = base_url.replace('index.html', 'index_831221_' + str(page_count - page_index) + '.html')
            yield scrapy.Request(url, method='GET', headers=self.headers, callback=self.parse_list)

    # 刷新分页的列表后的解析：获取每项政策详情链接，然后抓取详情
    def parse_list(self, response):
        item_list = parse_item_list(response.body)

        if not item_list:
            return False

        for item in item_list:
            url = item.get('url')
            print(threading.current_thread().name + ',抓取网页：' + url)
            if url is None:
                continue

            if CacheUtil.is_url_crawled(url):
                print('url：' + url + ' 已经抓取过，不重复抓取')
                continue

            full_url = url          # base_url.replace('index.html', '') + url
            yield scrapy.Request(full_url,
                                 method='GET',
                                 headers=self.headers,
                                 meta={'policy_item': item})

    # 默认解析器，在Request没有填写callback时调用：解析最后的详情，并发送到items及pipelines
    def parse(self, response):
        yield parse_policy_detail(response.body, response.meta['policy_item'])


# 计算页数
def parse_item_summary(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    table_tag = soup.find('table', {'class': 'pageN'})

    td_str = table_tag.find('td').text
    start_flag = 'maxPageNum = '
    end_flag = ';'
    start = td_str.find(start_flag)

    if start < 0:
        return start

    start += len(start_flag)
    end = td_str.find(end_flag, start)
    return int(td_str[start: end])


# 获取政策列表（分页）, 从1开始。同时支持首页和其他页
def parse_item_list(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    dl_tag = soup.find('span', {'id': 'comp_831221'})
    if dl_tag:
        dl_tag = dl_tag.find('dl')
    else:
        dl_tag = soup.find('dl')

    if not dl_tag:
        return []

    dd_tags = dl_tag.find_all('dd')

    if not dd_tags:
        return []

    policy_list = []
    for dd in dd_tags:
        a_tag = dd.find('a')
        if not a_tag:
            continue

        policy_list.append(PolicyItem(title=dd.text, url=(base_url.replace('index.html', '') + a_tag.attrs['href'])))

    return policy_list


# 根据链接爬取详情
def parse_policy_detail(page_text, item):
    if not item or not item.get('url'):
        return

    # 获取详情页
    soup = BeautifulSoup(page_text, "lxml")
    div_tag = soup.find('div', {'class': 'cmain'})
    if not div_tag or not div_tag.find('ul'):
        return

    li_tags = div_tag.find('ul').find_all('li')
    if not li_tags:
        return

    # 所有内容的<li>节)
    item['content'] = ''
    for p in li_tags:
        if p.text.find('相关链接') > 0:
            continue
        item['content'] += '\n<br>\n'
        item['content'] += p.text

    # 标题栏
    item['title'] = li_tags[0].text

    date_and_publisher = li_tags[1].text

    if str(date_and_publisher).__contains__('日期') and str(date_and_publisher).__contains__('来源'):
        # 发布日期
        item['date'] = str(date_and_publisher).split(' ')[0].strip()
        # 来源
        item['publisher'] = str(date_and_publisher).split(' ')[1].strip()
    else:
        # 发布日期
        item['date'] = date_and_publisher
        # 来源
        item['publisher'] = date_and_publisher

    return item


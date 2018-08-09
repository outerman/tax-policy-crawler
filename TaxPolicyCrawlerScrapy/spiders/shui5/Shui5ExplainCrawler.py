# coding=utf-8
import threading
import scrapy
from bs4 import BeautifulSoup
from TaxPolicyCrawlerScrapy.items import PolicyItem, PolicySource
from TaxPolicyCrawlerScrapy.util import CacheUtil, Constants

# 亿企赢-税屋，法规解读
# http://www.shui5.cn/article/FaGuiJieDu/
# 2017.11.2 共 110页8204条记录
base_url = 'http://www.shui5.cn'


class Shui5ExplainCrawler(scrapy.Spider):
    # 框架使用的属性，用于分类存储
    policy_source = PolicySource()
    doc_type = Constants.DocTypeShui5.doc_type
    policy_source['source'] = Constants.DocTypeShui5.source_name
    policy_source['policyType'] = Constants.DocTypeShui5.policy_types['policy_explain']  # '法规解读'

    # spider的名称，与setting配置里的一致；必须要有name属性，否则scrapy不做识别
    name = "Shui5ExplainCrawler"  # spider必须要有name属性，否则scrapy不做识别

    # 当前爬虫，request使用的headers
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #
    #     self.policy_source['source'] = '税屋'
    #     self.policy_source['policyType'] = '法规解读'

    def start_requests(self):
        yield scrapy.Request(base_url + '/article/FaGuiJieDu/', method='GET', headers=self.headers, callback=self.parse_main)
        # 测试带分页的
        # yield scrapy.Request('http://www.shui5.cn/article/FaGuiJieDu/12_110.html', method='GET', headers=self.headers,
        #                      callback=self.parse_list)

    # 刷新了主页后的解析：获取了cookies，下一步抓取分页总数summary
    def parse_main(self, response):
        if not response:
            return

        # 刷新列表首页后的解析：获取分页数，然后根据分页抓取
        print('获取分页信息：')
        page_count = parse_item_summary(response.body)
        print('page_count:' + str(page_count))

        if not page_count or page_count <= 0:
            print('获取"法规解读"失败，可能被禁止权限了。。。')
            return

        for index in range(1, page_count + 1):
            yield scrapy.Request(base_url + '/article/FaGuiJieDu/12_' + str(index) + '.html',
                                 method='GET',
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

            yield scrapy.Request(url,
                                 method='GET',
                                 headers=self.headers,
                                 meta={'policy_item': item})

    # 默认解析器，在Request没有填写callback时调用：解析最后的详情，并发送到items及pipelines
    def parse(self, response):
        # 详情页里，有可能也有翻页
        item = response.meta['policy_item']
        soup = BeautifulSoup(response.body, "lxml")
        if '$' not in item['url']:  # 如果含有$, 表示已经是翻页后的页面，不需要重复解析
            page_links_tag = soup.find('td', {'class': 'page_links'})
            if page_links_tag is not None:
                a_tags = page_links_tag.find_all('a')
                if a_tags is not None:
                    for a_tag in a_tags:
                        if '页' not in a_tag.text:
                            page_name = a_tag.attrs['href']
                            origin_page_name = page_name.split('$')[0] + '.' + page_name.split('.')[1]
                            url = item['url'].replace(origin_page_name, page_name)

                            new_item = PolicyItem(url=url, date=item['date'])
                            yield scrapy.Request(url,
                                                 method='GET',
                                                 headers=self.headers,
                                                 meta={'policy_item': new_item})

        yield get_policy_detail(soup, response.meta['policy_item'])


# 解析分页总数
def parse_item_summary(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    all_page_tags = soup.find_all('span', {'class': "pageinfo"})

    if not all_page_tags:
        return

    for spanTag in all_page_tags:
        strong_tags = spanTag.find_all('strong')

        if not strong_tags:
            continue

        page_size = int(strong_tags[0].text)  # 从第一个tr里分析页数
        if page_size >= 0:
            return page_size
    return 0


# 解析每页里的详情标题、链接
def parse_item_list(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    target_tag = soup.find('div', {'class': "arcList"})

    if not target_tag:
        return []

    ul_tags = target_tag.find_all('ul')

    if not ul_tags:
        return []

    policy_list = []
    for ul in ul_tags:
        all_li = ul.find_all('li')
        if len(all_li) <= 0:
            continue

        for li in all_li:
            a_tag = li.find('a')
            date_tag = li.find('span')
            if not a_tag or not date_tag:
                continue

            policy_list.append(PolicyItem(title=a_tag.text,
                                          url=base_url + a_tag.attrs['href'],
                                          date=date_tag.text))

    return policy_list


# 根据链接爬取详情
def get_policy_detail(soup, item):
    if not item or not item.get('url'):
        return

    # 标题
    title_tag = soup.find('div', {'class': "articleTitle"})
    if title_tag is not None:
        item['title'] = title_tag.text

    # 来源，作者
    publisher_tag = soup.find('div', {'class': "articleResource"})
    if publisher_tag is not None:
        item['publisher'] = publisher_tag.text.split('<script')[0]

    # 内容
    content_tag = soup.find('div', {'class': "arcContent"})
    if content_tag is not None:
        item['content'] = content_tag.text

    return item



# coding=utf-8
import threading
import scrapy
from bs4 import BeautifulSoup
from TaxPolicyCrawlerScrapy.items import PolicyItem


# 国税总局，政策解读
# http://www.chinatax.gov.cn/n810341/n810760/index.html
# 2017.9.8 约22页 * 25行每页 = 550行

base_url = 'http://www.chinatax.gov.cn/n810341/n810760/index.html'


class TaxPolicyExplainCrawler(scrapy.Spider):
    # 框架使用的属性
    name = 'TaxPolicyExplainCrawler'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

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
            yield scrapy.Request(base_url.replace('index.html', '') + url,
                                 method='GET',
                                 headers=self.headers,
                                 meta={'policy_item': item})

    # 默认解析器，在Request没有填写callback时调用：解析最后的详情，并发送到items及pipelines
    def parse(self, response):
        # TODO: cookiejar
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

        policy_list.append(PolicyItem(title=dd.text, url=a_tag.attrs['href']))

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
    # 发布日期
    item['date'] = li_tags[1].text
    # 来源
    item['publisher'] = li_tags[1].text

    return item


# # 从table的tr节里，获取文案
# def get_text_in_tr(tr_tag, index):
#     all_tds = tr_tag.find_all('td')
#     if len(all_tds) <= index:
#         return ''
#
#     td_str = all_tds[index]
#
#     return td_str.text
#
#
# # 结果输出到Excel
# def save_to_excel(policy_source, start_index, item_list):
#     with lock:
#         filename = 'TaxPolicyExplain.xls'
#         sheet_name = '税收政策'
#         is_reset = start_index == 0
#         # 先删除目标文件
#         if os.path.exists(filename) and is_reset:
#             os.remove(filename)
#
#         if os.path.exists(filename):
#             # 打开Excel
#             rdbook = xlrd.open_workbook(filename)
#             book = copy(rdbook)
#             excel_sheet = book.get_sheet(0)
#         else:
#             # 生成导出文件
#             book = xlwt.Workbook()
#             excel_sheet = book.add_sheet(sheet_name)
#
#         # 标题行
#         if is_reset:
#             excel_sheet.write(0, 0, '序号')
#             excel_sheet.write(0, 1, '政策来源')
#             excel_sheet.write(0, 2, '政策类型')
#             excel_sheet.write(0, 3, '税种')
#             excel_sheet.write(0, 4, '标题')
#             excel_sheet.write(0, 5, '副标题')
#             excel_sheet.write(0, 6, '链接地址')
#             excel_sheet.write(0, 7, '发文日期')
#             excel_sheet.write(0, 8, '正文内容')
#             excel_sheet.write(0, 9, '发文部门')
#
#         for i in range(1, len(item_list) + 1):
#             row_item = item_list[i - 1]
#             excel_sheet.write(start_index + i, 0, start_index + i)
#             excel_sheet.write(start_index + i, 1, policy_source.source)
#             excel_sheet.write(start_index + i, 2, policy_source.policyType)
#             excel_sheet.write(start_index + i, 3, policy_source.taxLevel)
#
#             excel_sheet.write(start_index + i, 4, row_item.title)
#             excel_sheet.write(start_index + i, 5, row_item.subtitle)
#             excel_sheet.write(start_index + i, 6, row_item.url)
#             excel_sheet.write(start_index + i, 7, row_item.date)
#             excel_sheet.write(start_index + i, 8, row_item.content)
#             excel_sheet.write(start_index + i, 9, row_item.publisher)
#
#         book.save(filename)
#
#
# # 获取政策列表（分页）
# def get_page_size(tr_tag):
#     td_str = get_text_in_tr(tr_tag, 0)  # 获取第一个节点的字符串
#     start = td_str.find('页 1/') + len('页 1/')
#     if start < 0:
#         return start
#
#     end = td_str.find(' ', start)
#
#     return int(td_str[start: end])
#
#
# def crawl_by_page(index, page_size):
#     try:
#         start_time = time.time()
#         policy_source = PolicySource('国税总局', '政策解读', '')
#         request_util = get_request_util()  # 每页分开刷：不同代理、不同线程、重试单元
#         print(threading.current_thread().name + ',获取第' + str(index + 1) + '/' + str(page_size) + '页的列表数据')
#         item_list = get_item_list(request_util, index, page_size)  # 网站url从1开始
#
#         if not item_list:
#             return False
#
#         policy_list_page = []
#         for item in item_list:
#             print(threading.current_thread().name + ',抓取网页：' + item.url)
#             policy_list_page.append(get_policy_detail(request_util, item))
#             # 不能频率太快，否则会被禁止访问, 随机延迟1~3秒
#             time.sleep((1 + random.random() * 2))
#
#         # saveToExcel(policy_source, start_index, policy_list_page)
#         # start_index += len(policy_list_page)
#         save_to_excel(policy_source, index * 20 + 1, policy_list_page)
#         print('finish crawling page ' + str(index) + '! take time:' + str(time.time() - start_time))
#         return True
#
#     except Exception as ex:
#         print('crawl_by_page generated an exception: %s' % str(ex))
#         return False
#
#
# def start_crawl():
#     page_count = get_item_summary()
#     print('page_size:' + str(page_count))
#
#     if not page_count or page_count <= 0:
#         print('获取政策解读首页，失败！')
#         return
#
#     # 测试一页
#     # page_count = 2
#
#     start_time = time.time()
#     # 每页分开刷：不同代理、不同线程、重试单元
#     page_index_to_crawl = [i for i in range(page_count)]
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         round_times = 1
#         while len(page_index_to_crawl) > 0:
#             print('crawl for %d th round' % round_times)
#             future_to_crawl = {executor.submit(crawl_by_page, index, page_count): index for index in
#                                page_index_to_crawl}
#             for future in concurrent.futures.as_completed(future_to_crawl):
#                 index = future_to_crawl[future]
#                 try:
#                     data = future.result()
#                     if data:
#                         page_index_to_crawl.remove(index)
#                 except Exception as exc:
#                     print('page %d crawl failed! %s' % (index, str(exc)))
#             round_times += 1
#         print('all complete! take time:' + str(time.time() - start_time))
#
#
# # 程序启动
# start_crawl()

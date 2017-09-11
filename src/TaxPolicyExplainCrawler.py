# coding=utf-8
import requests
import xlwt
import xlrd
from xlutils.copy import copy
import os
from bs4 import BeautifulSoup

# 国税总局，政策解读
# http://www.chinatax.gov.cn/n810341/n810760/index.html
# 2017.9.8 约22页 * 25行每页 = 550行
base_url = 'http://www.chinatax.gov.cn/n810341/n810760/index.html'


class PolicySource:
    source = ''         # 政策来源: 国税总局、各省市区税务局
    policyType = ''     # 政策类型：税收法规库、政策解读、与外国的税收条约
    taxLevel = ''       # 税种：国税、地税

    def __init__(self, policyType, source, taxLevel):
        self.policyType = policyType
        self.source = source
        self.taxLevel = taxLevel


class PolicyItem:
    title = ''          # 标题: 国家税务总局关于卷烟消费税计税价格核定管理有关问题的公告
    subtitle = ''       # 副标题：国家税务总局公告2017年第32号
    date = ''           # 发文日期
    content = ''        # 正文内容
    publisher = ''      # 发文部门
    url = ''            # 链接地址

    def __init__(self, title, url, subtitle, date, content, publisher):
        self.title = title
        self.url = url
        self.subtitle = subtitle
        self.date = date
        self.content = content
        self.publisher = publisher


# 从table的tr节里，获取文案
def getTextInTr(tr_tag, index):
    all_tds = tr_tag.find_all('td')
    if len(all_tds) <= index:
        return ''

    td_str = all_tds[index]

    return td_str.text


# 结果输出到Excel
def saveToExcel(policy_source, start_index, item_list):
    filename = 'TaxPolicy.xls'
    sheet_name = '税收政策'
    is_reset = start_index == 0
    # 先删除目标文件
    if os.path.exists(filename) and is_reset:
        os.remove(filename)

    if os.path.exists(filename):
        # 打开Excel
        rdbook = xlrd.open_workbook(filename)
        book = copy(rdbook)
        excel_sheet = book.get_sheet(0)
    else:
        # 生成导出文件
        book = xlwt.Workbook()
        excel_sheet = book.add_sheet(sheet_name)

    # 标题行
    if is_reset:
        excel_sheet.write(0, 0, '序号')
        excel_sheet.write(0, 1, '政策来源')
        excel_sheet.write(0, 2, '政策类型')
        excel_sheet.write(0, 3, '税种')
        excel_sheet.write(0, 4, '标题')
        excel_sheet.write(0, 5, '副标题')
        excel_sheet.write(0, 6, '链接地址')
        excel_sheet.write(0, 7, '发文日期')
        excel_sheet.write(0, 8, '正文内容')
        excel_sheet.write(0, 9, '发文部门')

    for i in range(1, len(item_list) + 1):
        row_item = item_list[i - 1]
        excel_sheet.write(start_index + i, 0, start_index + i)
        excel_sheet.write(start_index + i, 1, policy_source.source)
        excel_sheet.write(start_index + i, 2, policy_source.policyType)
        excel_sheet.write(start_index + i, 3, policy_source.taxLevel)

        excel_sheet.write(start_index + i, 4, row_item.title)
        excel_sheet.write(start_index + i, 5, row_item.subtitle)
        excel_sheet.write(start_index + i, 6, row_item.url)
        excel_sheet.write(start_index + i, 7, row_item.date)
        excel_sheet.write(start_index + i, 8, row_item.content)
        excel_sheet.write(start_index + i, 9, row_item.publisher)

    book.save(filename)


# 刷新主页，获取session（包含cookies信息）
def getSession():
    session = requests.Session()
    session.get('http://hd.chinatax.gov.cn/guoshui/main.jsp')

    return session


# 获取政策列表（分页）
def get_page_size(tr_tag):
    td_str = getTextInTr(tr_tag, 0)  # 获取第一个节点的字符串
    start = td_str.find('页 1/') + len('页 1/')
    if start < 0:
        return start

    end = td_str.find(' ', start)

    return int(td_str[start: end])


def getItemSummary(session):
    page = session.get(base_url)

    soup = BeautifulSoup(page.text, "lxml")
    table_tag = soup.find('table', {'class': 'pageN'})

    td_str = table_tag.find('td').text
    start = td_str.find('总页数:')

    if start < 0:
        return start

    start += len('总页数:')
    return int(td_str[start:])


# 获取政策列表（分页）, 从1开始
def getItemList(session, page_index, page_count):
    if page_index == 1:
        page = session.get(base_url)
        soup = BeautifulSoup(page.text, "lxml")
        dl_tag = soup.find('span', {'id': 'comp_831221'}).find('dl')
    else:
        url = base_url.replace('index.html', 'index_831221_' + str(page_count - page_index + 1) + '.html')
        page = session.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        dl_tag = soup.find('dl')

    if not dl_tag:
        return

    dd_tags = dl_tag.find_all('dd')

    if not dd_tags:
        return

    policy_list = []
    for dd in dd_tags:
        a_tag = dd.find('a')
        if not a_tag:
            continue

        policy_list.append(PolicyItem(dd.text, a_tag.attrs['href'], '', '', '', ''))

    return list(policy_list)


# 根据链接爬取详情
def getPolicyDetail(session, item):
    if not item or not item.url:
        return

    # 获取详情页
    page = session.get(base_url.replace('index.html', '') + item.url)
    soup = BeautifulSoup(page.text, "lxml")
    div_tag = soup.find('div', {'class': 'main'})
    if not div_tag or div_tag.find('ul'):
        return

    li_tags = div_tag.find('ul').find_all('li')
    if not li_tags:
        return

    # 所有内容的<li>节)
    for p in li_tags:
        if p.text.find('相关链接') > 0:
            continue
        item.content += '\n<br>\n'
        item.content += p.text

    # 标题栏
    item.title = li_tags[0].text
    # 发布日期
    item.date = li_tags[1].text
    # 来源
    item.publisher = li_tags[1].text

    return item


def startCrawl():
    session = getSession()

    policy_source = PolicySource('国税总局', '政策解读', '')
    page_count = getItemSummary(session)
    print('page_size:' + str(page_count))

    # 测试一页
    page_size = 1
    start_index = 0
    for index in range(page_count):
        print('获取第' + str(index + 1) + '/' + str(page_count) + '页的数据')
        item_list = getItemList(session, str(index + 1), page_count)

        if not item_list:
            continue

        policy_list_page = []
        for item in item_list:
            policy_list_page.append(getPolicyDetail(session, item))

        saveToExcel(policy_source, start_index, policy_list_page)
        start_index += len(policy_list_page)


# 程序启动
startCrawl()

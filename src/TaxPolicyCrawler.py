# coding=utf-8
import requests
import time
import random
import xlwt
import xlrd
from xlutils.copy import copy
import os
from bs4 import BeautifulSoup


# 国税总局，税收法规库的抓取
# http://hd.chinatax.gov.cn/guoshui/main.jsp
# 2017.9.8 共3531项查询结果236页
base_url = 'http://hd.chinatax.gov.cn/guoshui'


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
    start = td_str.find('页 1/')

    if start < 0:
        return start

    start += len('页 1/')
    end = td_str.find(' ', start)

    return int(td_str[start: end])


def getItemSummary(session):
    form_data = {'articleField01': '',
                 'articleField03': '',
                 'articleField04': '',
                 'articleField05': '',
                 'articleField06': '',
                 'articleField07_d': '',
                 'articleField07_s': '',
                 'articleField08': '',
                 'articleField09': '',
                 'articleField10': '',
                 'articleField11': '',
                 'articleField12': '',
                 'articleField13': '',
                 'articleField14': '',
                 'articleField18': '否',
                 'articleRole': '0000000',
                 'intvalue': '-1',
                 'intvalue1': '4',
                 'channelId': '',
                 'rtoken': 'fgk',
                 'shuizhong': '总局法规'}
    page = session.post(base_url + '/action/InitNewArticle.do', form_data)

    soup = BeautifulSoup(page.text, "lxml")
    all_table_tags = soup.find_all('table')

    if not all_table_tags:
        return

    for tableTag in all_table_tags:
        tr_tags = tableTag.find_all('tr')

        if not tr_tags:
            continue

        page_size = get_page_size(tr_tags[0])   # 从第一个tr里分析页数
        if page_size >= 0:
            return page_size

    return 0


# 获取政策列表（分页）, 从1开始
def getItemList(session, page_index):
    form_data = {'articleField01': '',
                 'articleField03': '',
                 'articleField04': '',
                 'articleField05': '',
                 'articleField06': '',
                 'articleField07_d': '',
                 'articleField07_s': '',
                 'articleField08': '',
                 'articleField09': '',
                 'articleField10': '',
                 'articleField11': '',
                 'articleField12': '',
                 'articleField13': '',
                 'articleField14': '',
                 'articleField18': '否',
                 'articleRole': '0000000',
                 'intvalue': '1',
                 'intvalue1': '4',
                 'intFlag': '0',
                 'cPage': page_index,
                 'rtoken': 'fgk',
                 'shuizhong': '总局法规'}
    page = session.post(base_url + '/action/InitNewArticle.do', form_data)
    soup = BeautifulSoup(page.text, "lxml")
    target_table = soup.find('table', {'cellspacing': "1"})

    if not target_table:
        return

    tr_tags = target_table.find_all('tr')

    if not tr_tags:
        return

    policy_list = []
    for tr in tr_tags:
        all_tds = tr.find_all('td')
        if len(all_tds) <= 0:
            continue

        a_tag = all_tds[0].find('a')
        if not a_tag:
            continue

        policy_list.append(PolicyItem(a_tag.text, a_tag.attrs['href'], all_tds[2].text, all_tds[1].text, '', ''))

    return list(policy_list)


# 根据链接爬取详情
def getPolicyDetail(session, item):
    if not item or not item.url:
        return

    # 获取详情页
    page = session.get(base_url + item.url[2:])
    soup = BeautifulSoup(page.text, "lxml")
    all_table_tags = soup.find_all('tbody')
    if not all_table_tags or len(all_table_tags) < 3:
        return

    # 找到td
    target_td = all_table_tags[2].find('td')

    # 所有内容的<p>节
    content_p_list = target_td.find_all('p')
    for p in content_p_list:
        item.content += '\n<br>\n'
        item.content += p.text

    # 签名的<p>节
    publisher_p_list = target_td.find_all('p', style=True)
    for p in publisher_p_list:
        item.publisher += '\n<br>\n'
        item.publisher += p.text

    return item


def startCrawl():
    session = getSession()

    policy_source = PolicySource('国税总局', '税收法规库', '')
    page_size = getItemSummary(session)
    print('page_size:' + str(page_size))

    if not page_size:
        print('获取税收法规库信息失败，可能被禁止权限了。。。')
        return

    # 测试一页
    page_size = 1
    start_index = 0
    for index in range(page_size):
        print('获取第' + str(index + 1) + '/' + str(page_size) + '页的数据')
        item_list = getItemList(session, str(index + 1))    # 网站url从1开始

        if not item_list:
            continue

        policy_list_page = []
        for item in item_list:
            print('抓取网页：' + item.url)
            policy_list_page.append(getPolicyDetail(session, item))
            # 不能频率太快，否则会被禁止访问, 随机延迟3~5秒
            time.sleep((3 + random.random() * 2))

        saveToExcel(policy_source, start_index, policy_list_page)
        start_index += len(policy_list_page)


# 程序启动
startCrawl()

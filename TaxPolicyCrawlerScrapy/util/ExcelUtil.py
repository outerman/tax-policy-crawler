# coding=utf-8

# Excel操作管理类，主要用于把爬取结果保存到Excel
import os
import threading

import xlrd
import xlwt
from xlutils.copy import copy

lock = threading.Lock()     # 线程同步锁，控制Excel写操作


# 结果输出到Excel
def save_to_excel(index_name, doc_type, item_list, is_reset=False):
    with lock:
        filename = index_name + '.xls'
        sheet_name = doc_type

        # 先删除目标文件
        if os.path.exists(filename) and is_reset:
            os.remove(filename)

        if os.path.exists(filename):
            # 打开Excel
            rdbook = xlrd.open_workbook(filename)
            i = list(rdbook.sheet_names()).index(sheet_name)    # 确定页签index
            book = copy(rdbook)
            # 如果页签存在，则读取该页，否则新增页签
            if i >= 0:
                excel_sheet = book.get_sheet(i)
            else:
                excel_sheet = book.add_sheet(sheet_name)

            is_create = False
        else:
            # 生成导出文件
            book = xlwt.Workbook()
            excel_sheet = book.add_sheet(sheet_name)
            is_create = True

        # 标题行
        if is_create:
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

        # 获取当前行数，往后追加
        start_index = len(excel_sheet.rows)

        for i in range(len(item_list)):
            row_item = item_list[i - 1]
            excel_sheet.write(start_index + i, 0, start_index + i)
            excel_sheet.write(start_index + i, 1, row_item.get('source'))
            excel_sheet.write(start_index + i, 2, row_item.get('policyType'))
            excel_sheet.write(start_index + i, 3, row_item.get('taxLevel'))

            excel_sheet.write(start_index + i, 4, row_item.get('title'))
            excel_sheet.write(start_index + i, 5, row_item.get('subtitle'))
            excel_sheet.write(start_index + i, 6, row_item.get('url'))
            excel_sheet.write(start_index + i, 7, row_item.get('date'))
            excel_sheet.write(start_index + i, 8, row_item.get('content'))
            excel_sheet.write(start_index + i, 9, row_item.get('publisher'))

        book.save(filename)

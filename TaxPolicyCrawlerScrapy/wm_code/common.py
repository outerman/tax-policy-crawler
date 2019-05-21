#!/usr/bin/env python
'''
Created on 2018年10月12日

@author: Administrator
'''

import os
import imp
from importlib._bootstrap import _exec, _load
from importlib import machinery
from importlib import util
import sys
import random
import requests
import time
import datetime
from dateutil.relativedelta import *
import re
import json
import configparser
import socket
import hashlib
from urllib.parse import *


EXE_NAME = sys.executable  # 当前运行的exe名称
SYS_PATCH = os.getcwd()  # 当前工作目录
if os.path.basename(EXE_NAME) != 'python.exe':
    SYS_PATCH = os.path.dirname(EXE_NAME)
    os.chdir(SYS_PATCH)


# 分割字符串
def diy_split(s, delimiter = ".", pairs_of_symbols = True, quotechar = True):
    _kh_count = 0
    _dkh_count = 0
    _zkh_count = 0

    def _is_pairs_of_symbols(c):
        nonlocal _kh_count
        nonlocal _dkh_count
        nonlocal _zkh_count
        if pairs_of_symbols:
            if c == '{':
                _dkh_count += 1
            if c == '}':
                _dkh_count -= 1
            if c == '[':
                _zkh_count += 1
            if c == ']':
                _zkh_count -= 1
            if c == '(':
                _kh_count += 1
            if c == ')':
                _kh_count -= 1
        return (_kh_count == 0) and (_dkh_count == 0) and (_zkh_count == 0)

    result = []
    value = ''
    skip1 = False
    skip2 = False
    for s_char in s:
        if quotechar:
            if not skip2 and (s_char == '"'):
                skip1 = not skip1
            if not skip1 and (s_char == "'"):
                skip2 = not skip2
        if _is_pairs_of_symbols(s_char) and not skip1 and not skip2 and (s_char == delimiter):
            result.append(value)
            value = ''
        else:
            value = value + s_char
    if value.strip() != '':
        result.append(value)
    return result

# 判断是否是字符串
def is_string(s):
    s1 = s.strip()
    if ((s1[0] == "'") and (s1[-1] == "'")) or ((s1[0] == '"') and (s1[-1] == '"')):
        skip1 = False
        skip2 = False
        index = 0
        for s_char in s1:
            index += 1
            if not skip2 and (s_char == '"'):
                skip1 = not skip1
            if not skip1 and (s_char == "'"):
                skip2 = not skip2
            if (not skip1 and not skip2) and (index != len(s1)):
                return False
        if not skip1 and not skip2:
            return True
    return False

# 判断是否是成对符号
def is_double_symbol(s):
    _kh_count = 0
    _dkh_count = 0
    _zkh_count = 0

    def _is_pairs_of_symbols(c):
        nonlocal _kh_count
        nonlocal _dkh_count
        nonlocal _zkh_count
        if c == '{':
            _dkh_count += 1
        if c == '}':
            _dkh_count -= 1
        if c == '[':
            _zkh_count += 1
        if c == ']':
            _zkh_count -= 1
        if c == '(':
            _kh_count += 1
        if c == ')':
            _kh_count -= 1
        return (_kh_count == 0) and (_dkh_count == 0) and (_zkh_count == 0)

    s1 = s.strip()
    if ((s1[0] == "{") and (s1[-1] == "}")) or ((s1[0] == "[") and (s1[-1] == "]")) or (
            (s1[0] == "(") and (s1[-1] == ")")) or ((s1[0] == "'") and (s1[-1] == "'")) or ((s1[0] == '"') and (s1[-1] == '"')):
        skip1 = False
        skip2 = False
        index = 0
        for s_char in s1:
            index += 1
            if not skip2 and (s_char == '"'):
                skip1 = not skip1
            if not skip1 and (s_char == "'"):
                skip2 = not skip2
            if _is_pairs_of_symbols(s_char) and not skip1 and not skip2 and (index != len(s1)):
                return False
        if _is_pairs_of_symbols('') and not skip1 and not skip2:
            return True
    return False


# 删除最外层双引号或单引号
def delete_quotechar(s):
    s1 = s.strip()
    if ((s1[0] == "'") and (s1[-1] == "'")) or ((s1[0] == '"') and (s1[-1] == '"')):
        if is_double_symbol(s1):
            return s1[1:-1]
    return s

# 删除最外层大括号、中括号或括号
def delete_double_symbol(s):
    s1 = s.strip()
    if ((s1[0] == "{") and (s1[-1] == "}")) or ((s1[0] == "[") and (s1[-1] == "]")) or (
            (s1[0] == "(") and (s1[-1] == ")")):
        if is_double_symbol(s1):
            return s1[1:-1]
    return s

# 逻辑关系解析
def parsing_judgment(condition):
    logical = ''
    param1 = ''
    param2 = ''
    skip1 = False
    skip2 = False
    for s_char in condition:
        if not skip2 and (s_char == "'"):
            skip1 = not skip1
        if not skip1 and (s_char == '"'):
            skip2 = not skip2
        if not skip1 and not skip2 and (s_char in ['=', '>', '<', '!', '≈']):
            logical = logical + s_char
            if param1 == '':
                param1 = param2
            param2 = ''
        else:
            param2 = param2 + s_char
    return delete_quotechar(param1), delete_quotechar(logical), delete_quotechar(param2)

# 逻辑表达式解析
def judgment_condition(param1, logical, param2):
    result = False
    if logical == '≈≈':
        result = param1.find(param2) != -1
    elif logical == '!=':
        result = (param1 != param2)
    elif logical == '==':
        result = (param1 == param2)
    elif logical == '>=':
        result = (param1 >= param2)
    elif logical == '>':
        result = (param1 > param2)
    elif logical == '<=':
        result = (param1 <= param2)
    elif logical == '<':
        result = (param1 < param2)
    return result

# 逻辑语句解析
def parsing_judgments(conditions):
    result = False
    condition = ''
    logical_and = False
    logical_or = False
    skip1 = False
    skip2 = False
    index = -1
    kh_count = 0
    skip_count = 0
    condition_s = delete_double_symbol(conditions.strip())
    for s_char in condition_s:
        index += 1
        if skip_count > 0:
            skip_count -= 1
            continue
        if not skip2 and (s_char == "'"):
            skip1 = not skip1
        if not skip1 and (s_char == '"'):
            skip2 = not skip2
        if not skip1 and not skip2:
            if s_char == '(':
                kh_count += 1
            if s_char == ')':
                kh_count -= 1
            if kh_count == 0:
                and_str = condition_s[index: index + 5].lower()
                or_str = condition_s[index: index + 4].lower()
                logical_and = (and_str == ' and ') or (and_str == ')and ') or (and_str == ')and(') or (and_str == ' and(')
                logical_or = (or_str == ' or ') or (or_str == ')or ') or (or_str == ')or(') or (or_str == ' or(')
                if logical_and or logical_or:
                    condition = condition + s_char
                    result = parsing_judgments(condition)
                    condition = ''
                    if logical_and:
                        skip_count = 3
                    if logical_or:
                        skip_count = 2
                    if result and logical_or:
                        return True
                    elif not result and logical_and:
                        return False
        condition = condition + s_char

    if condition.strip() != '':
        param1, logical, param2 = parsing_judgment(condition)
        result = judgment_condition(param1, logical, param2)
    return result

# 删除注解语句
def delete_annotation(str_line):
    result = ''
    skip_1 = False
    skip_2 = False
    for s_char in str_line:
        if not skip_2 and (s_char == '"'):
            skip_1 = not skip_1
        if not skip_1 and (s_char == "'"):
            skip_2 = not skip_2
        if not skip_1 and not skip_2 and (s_char == '#'):
            break
        result = result + s_char
    return result

# 通用加载文本函数，支持字符编码(tfAnsi, tfUnicode, tfUnicodeBigEndian, tfUtf8)
def load_txt_file(file_path):
    result = ''
    if os.path.isfile(file_path):
        # ($0000, $FFFE, $FEFF, $EFBB) (tfAnsi, tfUnicode, tfUnicodeBigEndian, tfUtf8);
        file = open(file_path, 'rb')
        try:
            b_result = file.read()
            if b_result[:3] == b'\xef\xbb\xbf':     # utf-8
                result = b_result[3:].decode('utf-8')
            elif b_result[:2] == b'\xfe\xff':   # unicode big endian
                result = b_result[2:].decode('utf-16-be')
            elif b_result[:2] == b'\xff\xfe':   # unicode
                result = b_result[2:].decode('utf-16')
            else:   # ansi
                result = b_result.decode('ansi')
        finally:
            file.close()
            return result
    return result

def save_txt_file(file_path, data, is_json=False, encoding='utf-8'):
    result = False
    if data is None:
        return False
    dir = os.path.dirname(file_path)
    os.makedirs(dir, exist_ok=True)
    file = open(file_path, 'w', encoding=encoding)
    try:
        if is_json:
            if not isinstance(data, str):
                data = json.dumps(data, ensure_ascii=False)
            else:
                data = json.dumps(eval(data), ensure_ascii=False)
        elif not isinstance(data, str):
            data = str(data)
        b_data = data.encode(encoding)
        if encoding == 'utf-8': # utf-8
            b_data = b'\xef\xbb\xbf' + b_data
        elif (encoding == 'utf-16-be') or (encoding == 'unicode big endian'):  # unicode big endian
            b_data = b'\xfe\xff' + b_data
        elif (encoding == 'utf-16') or (encoding == 'unicode'):  # unicode
            b_data = b'\xff\xfe' + b_data
        file.write(b_data.decode(encoding))
        result = True
    finally:
        file.close()
        return result

# 根据路径获取字典字段值
def get_dict_value_by_path(data_dict, path):
    if data_dict is None:
        return None
    names = path.split('.')
    result = data_dict
    for name in names:
        index = -1
        if (name.find('[') != -1) and (name[-1] == ']'):
            index = int(name[name.find('[') + 1:-1])
            name = name[:name.find('[')]
        if type(result) is dict:
            result = result.get(name, None)
        else:
            return None
        if (index != -1) and ((type(result) is list) or (type(result) is tuple)):
            result = result[index]
    if result != data_dict:
        return result
    return None

# 根据路径获取Json字段值
def get_json_value(data_json, path, default=''):
    result = get_dict_value_by_path(data_json, path)
    if result is None:
        result = default
    elif not (type(result) is str):
        result = str(result)
    return result

# 字符串转换
def convert_script(script_str, data_json):

    def _parsing_script(convert_str):
        script = convert_str[2:-2].strip()
        str_s = script.split(':', 1)
        if str_s[0] == 'json':
            return get_dict_value_by_path(data_json, str_s[1])
        return ''

    def _convert_script(line):
        str_line = line
        star = str_line.find('<%')
        while star != -1:
            end = str_line[star:].find('%>')
            if end != -1:
                end = star + end + 2
                convert_str = str_line[star:end]
                value = _parsing_script(convert_str)
                str_line = str_line[:star] + value + str_line[end:]
            star = str_line.find('<%')
        return str_line

    result = ''
    if script_str.strip() != '':
        lines = script_str.splitlines()
        for line in lines:
            line_str = delete_annotation(line)
            result = result + _convert_script(line_str)
    return result

# 文本内容转换
def convert_script_by_file(file_path, data_json):
    if os.path.exists(file_path):
        file_str = load_txt_file(file_path)
        return convert_script(file_str, data_json)
    return ''

# 从模块中查找函数并执行
def execute_func(object, func_path, *args, **kwargs):
    result = None
    objects = func_path.split('.')
    if len(objects) > 1:
        module_name = '.'.join(objects[:-1])
        func_name = objects[-1]
        if not (object is None):
            module_name = object.__name__ + '.' + module_name
        module_object = sys.modules[module_name]
    else:
        func_name = func_path
        module_object = object

    if not (module_object is None):
        if hasattr(module_object, func_name):
            func = getattr(module_object, func_name)
            if not (func is None):
                result = func(*args, **kwargs)
    return result

# 加载py包文件
def load_py_source(file_path, module_name=None):
    if os.path.isfile(file_path):
        if module_name is None:
            module_name = os.path.basename(file_path).split('.', 1)[0]
        spec = util.spec_from_file_location(module_name, file_path)
        if module_name in sys.modules:
            module = _exec(spec, sys.modules[module_name])
        else:
            module = _load(spec)
        # To allow reloading to potentially work, use a non-hacked loader which
        # won't rely on a now-closed file object.
        module.__loader__ = machinery.SourceFileLoader(module_name, file_path)
        module.__spec__.loader = module.__loader__
        return module
    return None

# 加载py包文件目录
def load_py_package(file_path, module_name=None):
    if os.path.isdir(file_path):
        extensions = (machinery.SOURCE_SUFFIXES[:] +
                      machinery.BYTECODE_SUFFIXES[:])
        for extension in extensions:
            init_path = os.path.join(file_path, '__init__' + extension)
            if os.path.exists(init_path):
                if module_name is None:
                    module_name = os.path.basename(file_path)
                file_path = init_path
                break
        else:
            raise ValueError('{!r} is not a package'.format(file_path))
    else:
        if module_name is None:
            module_name = os.path.basename(os.path.dirname(file_path))
    spec = util.spec_from_file_location(module_name, file_path, submodule_search_locations=[])
    if module_name in sys.modules:
        return _exec(spec, sys.modules[module_name])
    else:
        return _load(spec)

# 加载py模块，支持包、单文件两种方式
def load_py_module(file_path, module_name=None):
    if os.path.isdir(file_path):
        return load_py_package(file_path, module_name)
    elif os.path.isfile(file_path):
        file_name = os.path.basename(file_path).split('.', 1)[0]
        if file_name == '__init__':
            return load_py_package(file_path, module_name)
        else:
            return load_py_source(file_path, module_name)
    else:
        return None


def load_py_script(file_path):
    result = None
    module_name = os.path.basename(file_path).split('.', 1)[0]
    try:
        if module_name in sys.modules:
            result = sys.modules[module_name]
        else:
            result = imp.load_source(module_name, file_path)
    finally:
        return result

# 加载外部py文件并执行指定函数
def execute_py_script_func(file_path, func_name='main', *args, **kwargs):
    result = None
    mode = 'r'
    type_ = imp.PY_SOURCE
    file = None
    module_name = file_path
    try:
        module_name, suffix = os.path.splitext(os.path.basename(file_path))
        if suffix.strip() == '':
            type_ = imp.PKG_DIRECTORY
            if not os.path.isdir(file_path):
                print('模块路径不存：', file_path)
                return result
        else:
            if not os.path.isfile(file_path):
                print('模块文件不存：', file_path)
                return result
            file = open(file_path, 'rb')

        if module_name in sys.modules:
            module_obj = sys.modules[module_name]
        else:
            details = (suffix, mode, type_)
            module_obj = imp.load_module(module_name, file, file_path, details)

        if not(module_obj is None) and (func_name.strip() != ''):
            result = execute_func(module_obj, func_name, *args, **kwargs)
        else:
            if module_obj is None:
                print('没找到该模块：', module_name)
                raise Exception('没找到该模块：%s' % module_name)
            if func_name.strip() != '':
                print('函数名不能为空')
                raise Exception('函数名不能为空')

        return result
    except Exception as e:
        print('[execute_py_script_func]异常错误：', e)
        raise Exception('包文件[%s]加载失败, 错误原因：%s' % (module_name, str(e)))

# 生成随机字符串
def generate_random_str(randomlength=16, is_digit=False):
    # 生成一个指定长度的随机字符串
    random_str = ''
    if is_digit:
        base_str = '0123456789'
    else:
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

# 获取请求get内容
def requests_get(url, cookies=None, headers=None):
    def _compare_path(path1, path2):
        if path2 == '/':
            return True
        elif (len(path2) > 1) and (path1[:len(path2)] == path2):
            return True
        return False

    urldic = urlparse(url)
    cookie_s = {}
    if not (cookies is None):
        for cookie in cookies:
            cookie['path'] = cookie['path'].replace('//', '/')
            if (urldic.path.strip() != '') and (urldic.path.find('.') != -1):
                path = os.path.dirname(urldic.path) + '/'
            elif urldic.path.strip() == '':
                path = '/'
            else:
                path = urldic.path
            if not ('domain' in cookie.keys()) or (
                    (urldic.netloc.find(cookie['domain']) >= 0) and _compare_path(path, cookie['path'])):
                cookie_s[cookie['name']] = cookie['value']
    response = requests.get(url, cookies=cookie_s, headers=headers, verify=False)
    return response

# 获取请求post内容
def requests_post(url, cookies=None, headers=None, data=None, json=None):
    def _compare_path(path1, path2):
        if path2 == '/':
            return True
        elif (len(path2) > 1) and (path1[:len(path2)] == path2):
            return True
        return False

    urldic = urlparse(url)
    cookie_s = {}
    if not (cookies is None):
        for cookie in cookies:
            cookie['path'] = cookie['path'].replace('//', '/')
            if (urldic.path.strip() != '') and (urldic.path.find('.') != -1):
                path = os.path.dirname(urldic.path) + '/'
            elif urldic.path.strip() == '':
                path = '/'
            else:
                path = urldic.path
            if not ('domain' in cookie.keys()) or (
                    (urldic.netloc.find(cookie['domain']) >= 0) and _compare_path(path, cookie['path'])):
                cookie_s[cookie['name']] = cookie['value']

    response = requests.post(url, data=data, json=json, headers=headers, cookies=cookie_s, verify=False)
    print(response.text)
    return response

# 字符串转浮点值
def str_to_float_def(value, default=0.0):
    try:
        return float(value)
    except:
        return default

# 字符串转整数
def str_to_int_def(value, default=0):
    try:
        return int(value)
    except:
        return default

# 字符串转日期
def str_to_date_def(date_string, default=0):
    if date_string.find('-') != -1:
        date = re.match('\d\d\d\d\-\d*\-\d*', date_string)
        if not (date is None):
            return datetime.datetime.strptime(date.group(), "%Y-%m-%d")

    if date_string.find('\\') != -1:
        date = re.match('\d\d\d\d\\\d*\\\d*', date_string)
        if not (date is None):
            return datetime.datetime.strptime(date.group(), "%Y\%m\%d")

    return default

# 字符串转日期时间
def str_to_datetime_def(date_string, default=0):
    if date_string.find('-') != -1:
        date = re.match('\d\d\d\d\-\d*\-\d* \d*:\d*:\d*', date_string)
        if not (date is None):
            return datetime.datetime.strptime(date.group(), "%Y-%m-%d %H:%M:%S")

    if date_string.find('\\') != -1:
        date = re.match('\d\d\d\d\\\d*\\\d*', date_string)
        if not (date is None):
            return datetime.datetime.strptime(date.group(), "%Y\%m\%d %H:%M:%S")

    return str_to_date_def(date_string, default)


# 日期相对加减
def relativedelta_datetime(datetime, years=0, months=0, days=0, leapdays=0, weeks=0,
                 hours=0, minutes=0, seconds=0, microseconds=0,
                 year=None, month=None, day=None, weekday=None,
                 yearday=None, nlyearday=None,
                 hour=None, minute=None, second=None, microsecond=None):
    return datetime + relativedelta(years=years, months=months, days=days, leapdays=leapdays, weeks=weeks,
                 hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds,
                 year=year, month=month, day=day, weekday=weekday,
                 yearday=yearday, nlyearday=nlyearday,
                 hour=hour, minute=minute, second=second, microsecond=microsecond)


# 查找指定目录下的所有文件
def find_files(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# 取得MD5码方法，方法需要把文件全路径传递过来
def get_file_md5(filepath):
    # 打开文件，rb是打开方式：二进制只读形式打开
    f = None
    try:
        f = open(filepath, 'rb')
    except Exception as e:
        print(e)
        return ""
    # 定义一个MD5对象，名字叫md5_obj
    md5_obj = hashlib.md5()
    # 循环读取文件内容，一次读取8096个字节
    # 文件操作：必须是打开--读取--关闭的流程
    # 为了防止文件过大，一次读取文件一部分，效率高
    while True:
        d = f.read(8096)
        if not d:
            break
        # 将文件内容赋值给MD5对象，update方法支持分块多次调用
        md5_obj.update(d)
    # 获得MD5码
    hash_code = md5_obj.hexdigest()
    # 关闭文件。
    f.close()
    # 将MD5码转换为小写
    md5 = str(hash_code).lower()
    # 返回MD5码值
    return md5

# 获取时间戳
def get_time_stamp(unix=True, millisecond=True, date_farmat=False):
    ct = time.time()
    if unix:
        if millisecond:
            milliseconds = int(ct * 1000)
        else:
            milliseconds = int(ct)
        time_stamp = str(milliseconds)
    else:
        if date_farmat:
            format_date = "%Y-%m-%d %H:%M:%S"
            format_millisecond = "%s.%03d"
        else:
            format_date = "%Y%m%d%H%M%S"
            format_millisecond = "%s%03d"
        local_time = time.localtime(ct)
        data_head = time.strftime(format_date, local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = format_millisecond % (data_head, data_secs)
    return time_stamp

# 获取配置信息项的值
def get_cfg_option_value(file, section, option=None, default=''):
    if os.path.isfile(file):
        cf = configparser.ConfigParser()
        cf.read(file)
        if cf.has_section(section):
            if (option is None) or (option.strip() == ''):
                return cf.items(section)
            else:
                if cf.has_option(section, option):
                    return cf.get(section, option)
    return default

# 设置配置信息项的值
def set_cfg_option_value(file, section, option, value=None):
    if os.path.isfile(file):
        fp = open(file, 'r')
    else:
        fp = open(file, 'a+')
    try:
        cf = configparser.ConfigParser()
        cf.read_file(fp, file)
        if not cf.has_section(section):
            cf.add_section(section)
        cf.set(section, option, value)
        return cf.write(fp)
    finally:
        fp.close()


# 获取本地IP地址
def get_host_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

import getpass
import os
import socket
import time

import win32api
import win32clipboard

import psutil
import win32con

# from common import Config
# from common.PrintUtil import *
from TaxPolicyCrawlerScrapy.util import Config

conf = Config.get_system_conf()
try:
    sandbox_control_path = conf.get("sandbox", "sandbox_control_path")
    tax_client_path = conf.get("sandbox", "tax_client_path")
except:
    pass
ipaddress = ''


def get_clipboard_text():
    text = ""
    try:
        win32clipboard.OpenClipboard()
        dtext = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        text = dtext.decode('GBK')
    except Exception as e:
        print(str(e))
    return text


# 写入剪切板内容
def set_clipboard_text(string):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, string.encode('GBK'))
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(str(e))

# 结束沙盘
def terminate_sandbox(sandbox_name):
    try:
        full_cmd = sandbox_control_path + " /box:" + sandbox_name + " /terminate "
        print("关闭沙盘：%s" + full_cmd)
        os.popen(full_cmd)
    except Exception as e:
        print(e)


def startup_tax_client(sandbox_name):
    full_cmd = sandbox_control_path + " /box:" + sandbox_name + " /silent /nosbiectrl " + tax_client_path
    print("启动个税客户端：" + full_cmd)
    os.popen(full_cmd)


def get_host_ip():
    global ipaddress
    if ipaddress == '':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ipaddress = s.getsockname()[0]
        finally:
            s.close()
    return ipaddress


def get_user():
    return getpass.getuser()


def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


def get_cpu_state(interval=1):
    return psutil.cpu_percent(interval)


def get_memory_state():
    phymem = psutil.virtual_memory()
    return phymem.percent


def set_system_time(year=None, month=None, day=None):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime()
    try:
        win32api.SetSystemTime(year or tm_year, month or tm_mon, day or tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)
    except:
        print('时间设置失败！')

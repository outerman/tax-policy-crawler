import time
import win32api
import win32gui

import pykeyboard
import pymouse
import win32con

# from common import SystemUtil, RecordScreen
# from common.PrintUtil import *
from TaxPolicyCrawlerScrapy.util import SystemUtil

keyboard = pykeyboard.PyKeyboard()
mouse = pymouse.PyMouse()


# 键盘鼠标操作对象

def type_string(content, is_log=True):
    # RecordScreen.capture()
    caps_lock = win32api.GetKeyState(win32con.VK_CAPITAL)
    if caps_lock:
        print("大写状态开启")
        win32api.keybd_event(20, 0, 0, 0)  # caps lock
        win32api.keybd_event(20, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(0.2)
    keyboard.type_string(str(content))
    if is_log:
        print("输入：%s" % content)

    # RecordScreen.capture_after(0.5)


def press_alt_and(key):
    # RecordScreen.capture()
    keyboard.press_keys([keyboard.alt_key, key])
    # RecordScreen.capture_after()


def press_key(key):
    # RecordScreen.capture()
    keyboard.press_key(key)
    # RecordScreen.capture_after()


def press_ctrl_and(key):
    # RecordScreen.capture()
    keyboard.press_keys([keyboard.control_key, key])
    # RecordScreen.capture_after()


def press_paste(string=None):
    # RecordScreen.capture()
    if string:
        SystemUtil.set_clipboard_text(string)
        time.sleep(0.1)
    press_ctrl_and('v')

    # RecordScreen.capture_after()


def click_and_input(hwnd, x, y, content, is_log=False):
    click(hwnd, x, y)
    type_string(content, is_log)


def click(hwnd, x, y, button='l'):
    time.sleep(0.2)
    # RecordScreen.capture()
    # 定位屏幕的位置
    window_rect = win32gui.GetWindowRect(hwnd)
    print("点击窗体句柄 %d" % hwnd)
    screen_x = window_rect[0] + x
    screen_y = window_rect[1] + y

    click_screen(screen_x, screen_y, button)
    # RecordScreen.capture_after()


def click_screen(x, y, button='l'):
    # RecordScreen.capture()
    print("点击(%d,%d)" % (x, y))

    # 点击鼠标
    if button == 'l':
        mouse.click(x, y, 1, 1)
    elif button == 'r':
        mouse.click(x, y, 2, 1)

    # RecordScreen.capture_after()

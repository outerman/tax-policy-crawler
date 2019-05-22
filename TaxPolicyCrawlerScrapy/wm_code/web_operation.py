#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
'''
Created on 2019-01-25

@author: Administrator
'''
import random
import time

import datetime
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import win32api
import win32con

from TaxPolicyCrawlerScrapy.wm_code.wm_code import *
from TaxPolicyCrawlerScrapy.wm_code.common import *

WM_LIB_PASSWORD = "foresee2017"  # 完美验证码识别标识库密码
WM_LIBRARY_LIST = []

VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
    '`': 0xC0}


# 获取webdriver的类型
def get_browser_type(browser):
    return str(type(browser)).split(".")[2]


def web_find_element(element, field_id):  # 网页中查找元素  元素id或name
    if field_id.strip() != '':
        value = field_id.strip()
        try:
            html_element = element.find_element_by_id(value)
            if html_element is None:
                html_element = element.find_element_by_name(value)
            return html_element
        except:
            return None


# 多属性判断
def parsing_judgments_element(element, conditions):
    def _get_attribute_value(name):
        result = name.strip()
        if result[0] == '@':
            attribute_name = result[1:]
            if attribute_name == 'text':
                result = element.text
            else:
                result = element.get_attribute(attribute_name)
        return result

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
                logical_and = (condition_s[index: index + 2].lower() == '&&')
                logical_or = (condition_s[index: index + 2].lower() == '||')
                if logical_and or logical_or:
                    result = parsing_judgments(condition)
                    condition = ''
                    skip_count = 1
                    if result and logical_or:
                        return True
                    elif not result and logical_and:
                        return False
        condition = condition + s_char

    if condition.strip() != '':
        param1, logical, param2 = parsing_judgment(condition)
        param1 = _get_attribute_value(param1)
        param2 = _get_attribute_value(param2)
        result = judgment_condition(param1, logical, param2)
    return result


def web_find_elements(element, element_info, find_type='names'):  # 网页中查找元素  元素tagname或name
    attributes = diy_split(element_info.strip(), '@')
    action_name = delete_quotechar(attributes[0])
    del attributes[0]
    # print(attributes)
    if find_type == 'tagname':
        elements = element.find_elements_by_tag_name(action_name)
    elif find_type == 'names':
        elements = element.find_elements_by_tag_name(action_name)
    elif find_type == 'xpaths':
        elements = element.find_elements_by_xpath(action_name)
    if (elements is None) or (len(elements) == 0):
        return None
    if len(attributes) == 0:
        return elements
    rm = re.search('\[\d*\]', attributes[0])
    if not (rm is None):
        curr_element = elements[int(delete_double_symbol(rm.group()))]
    else:
        finded = False
        for curr_element in elements:
            for attribute in attributes:
                param1, logical, param2 = parsing_judgment(attribute)
                if param1 == 'text':
                    param1 = curr_element.text
                else:
                    param1 = curr_element.get_attribute(param1)
                if judgment_condition(param1, logical, param2):
                    finded = True
                    break
            if finded:
                break
        if not finded:
            return None
    return curr_element


def switch_web_window(browser, win_info=None):
    handles = browser.window_handles
    if (win_info is None) or (win_info.strip() == ''):
        try:
            browser.switch_to.window(handles[-1])
            print(browser.title, browser.current_url)
            return True
        except Exception as e:
            print('[switch_web_window]异常错误：', e)
            if (browser.title.find(win_info) != -1) or (browser.current_url.find(win_info) != -1):
                return True

    try:
        if (browser.title.find(win_info) == -1) and (browser.current_url.find(win_info) == -1):
            current_handle = browser.current_window_handle
            for i in range(2):
                handles = browser.window_handles
                for handle in handles:  # 切换窗口
                    if handle != current_handle:
                        try:
                            browser.switch_to.window(handle)
                        except Exception as e:
                            print('[switch_web_window]异常错误：', e)

                        if (browser.title.find(win_info) != -1) or (browser.current_url.find(win_info) != -1):
                            print(browser.title, browser.current_url)
                            return True
                # time.sleep(1)
            browser.switch_to.window(current_handle)
        return False
    except Exception as e:
        print('[switch_web_window]异常错误：', e)
        if 'Alert Text:' in str(e):
            return switch_web_window(browser, win_info)


def close_web_window(browser, win_info=None):
    result = False
    if (win_info is None) or (win_info.strip() == ''):
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        result = True
    else:
        if (browser.title.find(win_info) != -1) or (browser.current_url.find(win_info) != -1):
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            result = True
        else:
            current_handle = browser.current_window_handle
            handles = browser.window_handles
            for handle in handles:  # 切换窗口
                if handle != current_handle:
                    browser.switch_to.window(handle)
                    if (browser.title.find(win_info) != -1) or (browser.current_url.find(win_info) != -1):
                        browser.close()
                        result = True
                        break
            browser.switch_to.window(current_handle)

    if len(browser.window_handles) > 0:
        print(browser.title, browser.current_url)
    return result


def switch_web_alert(browser, actions):
    result = None
    try:
        alert = browser.switch_to_alert()
        result = alert
        if not (alert is None):
            for action in actions.split(","):
                if action.lower() == 'accept':
                    alert.accept()
                elif action.lower() == 'text':
                    result = alert.text
                elif action.lower() == 'dismiss':
                    alert.dismiss()
                time.sleep(0.1)
    finally:
        return result


def wait_and_find_element(browser, curr_element, timeout, action_str):
    start_time = time.time()
    n = 0
    try:
        while True:
            try:
                n += 1
                frame_layer_count, element = parsing_action(browser, curr_element, delete_quotechar(action_str))
                if not (element is None):
                    if type(element) is str:
                        if element.strip() != '':
                            break
                    else:
                        break

                return_switch_to_frame(browser, frame_layer_count)
                time.sleep(0.5)
                if timeout <= round(time.time() - start_time, 2):
                    return 0, None
                pass
            except:
                pass

        return frame_layer_count, element
    finally:
        print('等待查找[%d]次' % n)


def web_driver_wait(browser, timeout, action_str):
    try:
        time.sleep(float(action_str))
        return True
    except:
        start_time = time.time()
        n = 0
        try:
            while True:
                try:
                    n += 1
                    element = parsing_operate_web(browser, browser, delete_quotechar(action_str))
                    if not (element is None):
                        if type(element) is str:
                            if element.strip() != '':
                                return True
                        else:
                            return True

                    time.sleep(0.5)
                    if timeout <= round(time.time() - start_time, 2):
                        return False
                    pass
                except:
                    pass

            return False
        finally:
            print('等待查找[%d]次' % n)


# 等待网页加载，超时重刷新
def wait_driver_get(browser, timeout, action_str):
    start_time = time.time()
    while True:
        if web_driver_wait(browser, 20, action_str):
            break
        browser.refresh()
        time.sleep(1)
        if timeout <= round(time.time() - start_time, 2):
            return False
    return True


def web_wait(browser, timeout, action_str):
    print('正在执行等待语句[%s]...' % action_str)
    start_time = time.time()
    while True:
        frame_layer_count, element = parsing_action(browser, browser, delete_quotechar(action_str))
        try:
            if element is None:
                break
            else:
                try:
                    if not element.is_displayed():
                        break
                    else:
                        element = None
                except Exception as e:
                    print('[web_wait]异常错误：', e)
                    style = element.get_attribute('style')
                    if 'display: none;' in style:
                        break

        finally:
            return_switch_to_frame(browser, frame_layer_count)

        time.sleep(1)
        if timeout <= round(time.time() - start_time, 2):
            return None

    return element


def action_event(browser, element, event_str):
    events = diy_split(event_str, ",")
    result = None
    ie_mode = (get_browser_type(browser) == 'ie')
    for event in events:
        if event == 'click':
            element.click()
        elif event == 'jsclick':
            try:
                browser.set_script_timeout(1)
                browser.execute_script("arguments[0].click();", element)
            except Exception as e:
                print('弹出模态窗口点击占用超时：', e)
        elif event == 'lclick':
            ActionChains(browser).click(element).perform()
        elif event == 'dblclick':
            if ie_mode:
                element.click()
            ActionChains(browser).double_click(element).perform()
        elif event == 'submit':
            element.submit()
        elif event == 'enter':
            element.send_keys(Keys.ENTER)
        elif event == 'tab':
            element.send_keys(Keys.TAB)
        elif event == 'focus':
            browser.set_script_timeout(1)
            browser.execute_script("arguments[0].focus();", element)
        elif event == 'clear':
            element.clear()
        else:
            event_s = event.split('=', 1)
            event_type = event_s[0]
            event_value = None
            if len(event_s) == 2:
                event_value = delete_quotechar(event_s[1])
            if event_type[0] == '@':
                if event_value is None:
                    result = element.get_attribute(event[1:])
                else:
                    if event_type[1:] == 'value':
                        js_str = 'arguments[0].value="%s";' % event_value
                    else:
                        js_str = 'arguments[0].setAttribute("%s","%s");' % (event_type[1:], event_value)
                    browser.set_script_timeout(1)
                    browser.execute_script(js_str, element)
            elif event_type == 'value':
                if event_value is None:
                    result = element.get_attribute(event_type)
                else:
                    element.send_keys(event_value)
                    element.send_keys(Keys.TAB)
            elif event_type == 'text':
                if event_value is None:
                    result = element.text
                else:
                    element.text = event_value
            elif event_type == 'cookies':
                if event_value is None:
                    result = browser.get_cookies()
                else:
                    cookies = eval(event_value)
                    if len(cookies) > 0:
                        for cookie_dict in cookies:
                            # cookie_dict.pop('domain')
                            cookie_dict['path'] = cookie_dict['path'].replace('//', '/')
                            browser.add_cookie(cookie_dict)
            elif event_type == 'innerHTML':
                if event_value is None:
                    result = element.get_attribute('innerHTML')
                else:
                    browser.set_script_timeout(1)
                    browser.execute_script("arguments[0].innerHTML = '%s';" % event_value, element)
            elif event_type == 'select_value':
                Select(element).select_by_value(event_value)
            elif event_type == 'select_index':
                Select(element).select_by_index(event_value)
            elif event_type == 'select_text':
                Select(element).select_by_visible_text(event_value)
            elif event_type == 'checked':
                if element.is_selected() != (event_value.lower() == 'true'):
                    element.click()
            elif event_type == 'sleep':
                time.sleep(float(event_value))
            elif event_type == 'js':
                browser.set_script_timeout(1)
                if event_value.find('arguments[0]') != -1:
                    browser.execute_script(event_value, element)
                else:
                    browser.execute_script(js_str)
            elif event_type == 'send_keys':
                element.send_keys(event_value)
        # time.sleep(0.1)
    return result


def return_switch_to_frame(browser, layer_count=-1):
    if layer_count == -1:
        browser.switch_to.default_content()
    else:
        for i in range(layer_count):
            browser.switch_to.parent_frame()


# 设置窗口状态
def set_window_state(browser, state):
    if state.lower() == 'maximize':
        browser.maximize_window()
    elif state.lower() == 'minimize':
        browser.minimize_window()


def parsing_action(browser, element, actionstr):
    if actionstr.strip() == '':
        return None
    action_str = actionstr.replace("\\\'", "'")
    action_str = action_str.replace('\\\"', '"')
    frame_layer_count = 0
    result_element = None
    curr_element = element
    action_array = diy_split(action_str.strip(), '.')
    try:
        for action in action_array:
            action_s = action.split(':', 1)
            action_type = action_s[0].strip()
            action_name = ''
            if len(action_s) == 2:
                action_name = delete_quotechar(action_s[1].strip())
            if action_type == 'id':
                browser.implicitly_wait(1)
                curr_element = curr_element.find_element_by_id(action_name)
            elif action_type == 'name':
                browser.implicitly_wait(1)
                curr_element = curr_element.find_element_by_name(action_name)
            elif action_type == 'xpath':
                browser.implicitly_wait(1)
                curr_element = curr_element.find_element_by_xpath(action_name)
            elif (action_type == 'tagname') or (action_type == 'names') or (action_type == 'xpaths'):
                browser.implicitly_wait(3)
                curr_element = web_find_elements(curr_element, action_name, action_type)
            elif action_type == 'wait_find':
                layer_count, curr_element = wait_and_find_element(browser, curr_element, 20, action_name)
                frame_layer_count += layer_count
                continue
            elif action_type == 'parent':
                browser.implicitly_wait(1)
                curr_element = curr_element.find_element_by_xpath('./..')
                if curr_element is None:
                    break
                continue
            elif action_type == 'is_displayed':
                if not curr_element.is_displayed():
                    curr_element = None
                    break
                else:
                    continue
            elif action_type == 'is_enabled':
                if not curr_element.is_enabled():
                    curr_element = None
                    break
                else:
                    continue
            elif action_type == 'event':
                action_result = action_event(browser, curr_element, action_name)
                if not (action_result is None):
                    curr_element = action_result
                continue
            elif action_type == 'js':
                browser.execute_script(action_name)
                continue
            elif action_type == 'url':
                if frame_layer_count != 0:
                    return_switch_to_frame(browser, frame_layer_count)
                    curr_element = browser
                    frame_layer_count = 0
                browser.implicitly_wait(30)
                browser.get(action_name)
                continue
            elif action_type == 'window':
                if switch_web_window(browser, action_name):
                    browser.switch_to.default_content()
                    frame_layer_count = 0
                    curr_element = browser
                else:
                    curr_element = None
                    break
                continue
            elif action_type == 'window_close':
                close_web_window(browser, action_name)
                if frame_layer_count != 0:
                    frame_layer_count = 0
                curr_element = browser
                continue
            elif action_type == 'window_state':
                set_window_state(browser, action_name)
                continue
            elif action_type == 'return_frame':
                return_switch_to_frame(browser, int(action_name))
                continue
            elif action_type == 'alert':
                curr_element = switch_web_alert(browser, action_name)
                continue
            elif action_type == 'web_wait':
                web_wait(browser, 120, action_name)
                continue
            elif action_type == 'wait':
                if web_driver_wait(browser, 20, action_name):
                    continue
                else:
                    result_element = None
                    return
            elif action_type == 'wait_get':
                if wait_driver_get(browser, 120, action_name):
                    continue
                else:
                    result_element = None
                    return
            elif action_type == 'list':
                parsing_operate_web(browser, curr_element, delete_double_symbol(action_name))
                continue
            else:
                return None
            if curr_element is None:
                break
            if type(curr_element) is str:
                break
            if (str(type(curr_element)).find('WebElement') != -1) and curr_element.tag_name == 'iframe':
                browser.switch_to.frame(curr_element)
                curr_element = browser
                frame_layer_count += 1

        result_element = curr_element
    except Exception as e:
        result_element = None
        print('[parsing_action]异常错误：', e)
        # log_debug('异常报错：', e)
    finally:
        return frame_layer_count, result_element


def parsing_action_line(browser, element, actionstr):
    action_str = actionstr
    if action_str[-1] == ';':
        action_str = action_str[:-1]

    layer_count, result_element = parsing_action(browser, element, action_str)
    return_switch_to_frame(browser, layer_count)
    return result_element


def parsing_operate_web(browser, curr_element, actions):
    result = None
    if type(actions) is str:
        if actions.strip() == '':
            return result
        action_str = actions.replace('\n', '')
        action_array = diy_split(action_str, ';')
    elif type(actions) is list:
        action_array = actions
    else:
        return result
    for action in action_array:
        if action.strip() == '':
            continue

        start_time = time.time()
        result = parsing_action_line(browser, curr_element, action)
        print('已执行脚本[%ss]：%s;\n执行结果：%s' % (round(time.time() - start_time, 2), action, result))
    return result


def web_submit(web_object, submit_info):  # 提交按钮点击
    if submit_info.strip() == '':
        return False
    strarray = submit_info.split(',')
    tagname = strarray[0]
    valuetype = ''
    value = ''
    if len(strarray) > 1:
        valuetype = strarray[1]

    if len(strarray) > 2:
        value = strarray[2]

    html_elements = web_object.find_elements_by_tag_name(tagname.strip())
    for html_element in html_elements:
        if valuetype.upper() == 'src':
            if html_element.src.find(value) >= 0:
                html_element.click()
                return True
        else:
            if (html_element.classname.upper() == value) or (html_element.type.upper() == value):
                html_element.click()
                return True


def web_auto_login(web_object, username, password, veri_code, field_username, field_password, field_veri_code,
                   field_submit, javascript):  # 网页自动登陆
    b_result = False
    if (username == '') or (password == ''):
        return b_result

    try:
        if field_username.strip() != '':
            html_element = web_find_element(web_object, field_username)
            if not (html_element is None):
                html_element.clear()
                html_element.send_keys(username)

        if field_password.strip() != '':
            html_element = web_find_element(web_object, field_password)
            if not (html_element is None):
                if not html_element.is_displayed():
                    web_object.execute_script(
                        'document.getElementById(\"' + field_password + '\").style.display="block"')
                html_element.clear()
                html_element.send_keys(password)
            else:
                return b_result

        if field_veri_code.strip() != '':
            html_element = web_find_element(web_object, field_veri_code)
            if not (html_element is None):
                html_element.clear()
                html_element.send_keys(veri_code)
            else:
                return b_result

        if field_submit.strip() != '':
            if field_submit.find(',') >= 0:
                b_result = web_submit(web_object, field_submit)
            else:
                html_element = web_find_element(web_object, field_submit)
                if not (html_element is None):
                    if html_element.tag_name.upper() == 'form':
                        html_element.submit()
                    else:
                        html_element.click()
                    b_result = True
            return b_result
        elif javascript.strip() != '':
            web_object.execute_script(javascript)
            b_result = True

        return b_result
    except Exception:
        pass


def download_file(url, cookie_list=None):  # 验证码图片下载
    def _compare_path(path1, path2):
        if path2 == '/':  # path1 == path2:
            return True
        elif (len(path2) > 1) and (path1[:len(path2)] == path2):
            return True
        return False

    urldic = urlparse(url)
    cookies = {}
    if not (cookie_list is None):
        for cookie in cookie_list:
            cookie['path'] = cookie['path'].replace('//', '/')
            if (urldic.path.strip() != '') and (urldic.path.find('.') != -1):
                path = os.path.dirname(urldic.path) + '/'
            elif urldic.path.strip() == '':
                path = '/'
            else:
                path = urldic.path
            if not ('domain' in cookie.keys()) or (
                    (urldic.netloc.find(cookie['domain']) >= 0) and _compare_path(path, cookie['path'])):
                if (cookie['name'] in cookies) and (cookie['path'] == '/'):
                    continue
                cookies[cookie['name']] = cookie['value']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'
    }
    response = requests.get(url, cookies=cookies, headers=headers, verify=False)
    return response


# 操作滑块移动
def move_to_slider(browser, slider_element, move_len):
    action = ActionChains(browser)
    action.move_to_element(slider_element)
    action.click_and_hold(slider_element).perform()  # 鼠标左键按下不放
    action.reset_actions()
    times = 5
    i = times
    tx = move_len
    while i > 0:
        # time.sleep(1)
        time.sleep(random.randint(5, 10) / 20)
        of = move_len / times
        tx = tx - of
        print(of)
        action.move_by_offset(of, 0).perform()
        action.reset_actions()
        # action._actions.pop()#加上这句就没有问题啦
        i = i - 1
    time.sleep(0.1)
    action.release().perform()
    time.sleep(2)


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def mouse_lclick(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def mouse_dblclick(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


def mouse_absolute(x, y, x2, y2):
    SW = 1377
    SH = 768
    windll.user32.SetCursorPos(x, y)  # 鼠标移动到
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 左键按下
    time.sleep(0.2)
    mw = int(x2 * 65535 / SW)
    mh = int(y2 * 65535 / SH)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE + win32con.MOUSEEVENTF_MOVE, mw, mh, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def key_input(str=''):
    for c in str:
        win32api.keybd_event(VK_CODE[c], 0, 0, 0)
        win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.01)


# 操作滑块移动
def mouse_move_to_slider(frame_pos, element, move_len, step_len=50):
    elementwidth = element.size['width']
    elementheight = element.size['height']
    x1 = frame_pos[0] + int(element.location['x']) + elementwidth // 2
    y1 = frame_pos[1] + int(element.location['y']) + elementheight // 2
    x2 = x1 + move_len
    # mouse_move(x1, y1)
    mouse_absolute(x1, y1, x2, y1)


'''
# 操作滑块验证
def slider_captcha(browser, captcha_id, slider_id, frame_pos = (0, 0)):
    result = False
    captcha_elem = web_find_element(browser, captcha_id)
    if not (captcha_elem is None):
        captchawidth = captcha_elem.size['width']
        captcha_src = captcha_elem.get_attribute('src')
        captcha_response = download_file(captcha_src)
        if captcha_response.status_code == 200:
            print(len(captcha_response.content))
            if len(captcha_response.content) == 0:
                return False
            now_time = datetime.datetime.now()
            now_time_str = datetime.datetime.strftime(now_time, '%y%m%d%h%m%s')
            cwdir = SYS_PATCH #os.getcwd()
            tempdir = cwdir + "\\bin\captcha"
            if not os.path.exists(tempdir):
                os.makedirs(tempdir)
            imgpath = tempdir + "\\slider_" + now_time_str + ".jpg"
            with open(imgpath, 'wb') as f:
                f.write(captcha_response.content)
                f.close()
            image_1 = Image.open(imgpath, "r")
            img_array = find_image_outline_by_img(image_1, 220, 255)
            rect = get_square(img_array, 90, 90, 80)
            distance = rect[0][0]
            m_len = int(distance * (captchawidth / image_1.size[0]))
            print(distance, image_1.size[0], captchawidth)
            # image1.show()
    # mlen = int(input("请输入移动距离："))
    slider_element = web_find_element(browser, slider_id)
    if not (slider_element is None):
        if get_browser_type(browser) == 'ie':
            m_len = m_len - (int(slider_element.location['x']) - int(captcha_elem.location["x"]))
            mouse_move_to_slider(frame_pos, slider_element, m_len)
        else:
            m_len = m_len - 30
            move_to_slider(browser, slider_element, m_len)
        print(m_len)
        result = True
    return result

# 处理验证码弹窗
def get_captcha(browser, damatuinstance):
    iframelst = browser.find_elements_by_tag_name('iframe')
#     print(f"captchahandler: enter , iframelst = {iframelst}")
    for iframe in iframelst:
        iframeid = iframe.get_attribute('id')
        iframesrc = iframe.get_attribute('src')
#         print(f"captchahandler: iframeid = {iframeid}, iframesrc = {iframesrc}")
        # 找到验证码登录iframe
        if iframeid and iframeid.find('dialog') != -1:
            if iframesrc and iframesrc.find(r'sec.1688.com') != -1:
                # 拿到iframe的宽度和高度
                framewidth = iframe.size['width']
                frameheight = iframe.size['height']

                # 代表验证码区域可见
                # 某些情况下，会出现验证码框不弹出，而iframe还在的暂态
                if framewidth > 0 and frameheight > 0:
                    #                     print(f"验证码弹出, 进行处理, framewidth = {framewidth}, frameheight = {frameheight}")
                    # 截屏，在chrome中截取的是可视区域，而不是整个html页面
                    # 前提是当前project下已经创建了clawerimgs目录
                    browser.get_screenshot_as_file('clawerimgs/screenshot.png')

                    # 先拿到iframe在整个可视页面（也就是上面的截屏）中的相对位置，因为前面对页面的窗口大小进行了设置960 x 960
                    # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标
                    # location 拿到的是相对整个html页面的坐标
                    framex = int(iframe.location_once_scrolled_into_view['x'])
                    framey = int(iframe.location_once_scrolled_into_view['y'])

                    # print(f"captchahandler: framex = {framex}, framey = {framey}, framewidth = {framewidth}, frameheight = {frameheight}")
                    # 获取指定元素位置，先拿iframe元素的图片
                    left = framex
                    top = framey
                    right = framex + framewidth
                    bottom = framey + frameheight

                    # 通过image处理图像，截取frame的图片 ———— 无意义，只是做经验总结
                    imgframe = Image.open('clawerimgs/screenshot.png')
                    imgframe = imgframe.crop((left, top, right, bottom))  # 裁剪
                    imgframe.save('clawerimgs/iframe.png')

                    # 切换到验证码弹出框的frame，不然无法获取到验证码元素，因为验证码元素是在iframe中
                    browser.switch_to.frame(iframe)

                    # ------获取验证码图片，第一种方法：在frame区域截取
                    # 获取指定元素位置
                    captchaelem = browser.find_element_by_xpath(
                        "//img[contains(@id, 'checkcodeimg')]")
                    # 因为验证码在frame中没有缩放，直接取验证码图片的绝对坐标
                    # 这个坐标是相对于它所属的frame的，而不是整个可视区域
                    captchax = int(captchaelem.location['x'])
                    captchay = int(captchaelem.location['y'])

                    # 取验证码的宽度和高度
                    captchawidth = captchaelem.size['width']
                    captchaheight = captchaelem.size['height']

                    captcharight = captchax + captchawidth
                    captchabottom = captchay + captchaheight
                    # print(f"captchahandler: 1 captchax = {captchax}, captchay = {captchay}, captchawidth = {captchawidth}, captchaheight = {captchaheight}")
                    # 通过image处理图像，第一种方法：在frame区域截取
                    imgobject = Image.open('clawerimgs/iframe.png')
                    imgcaptcha = imgobject.crop(
                        (captchax, captchay, captcharight, captchabottom))      # 裁剪
                    imgcaptcha.save('clawerimgs/captcha1.png')

                    # ------获取验证码图片，第二种方法：在整个可视区域截取。 就要加上这个iframe的便宜量
                    captchaelem = browser.find_element_by_xpath(
                        "//img[contains(@id, 'checkcodeimg')]")
                    captchax = int(captchaelem.location['x']) + framex
                    captchay = int(captchaelem.location['y']) + framey
                    captchawidth = captchaelem.size['width']
                    captchaheight = captchaelem.size['height']
                    captcharight = captchax + captchawidth
                    captchabottom = captchay + captchaheight
                    # print(f"captchahandler: 2 captchax = {captchax}, captchay = {captchay}, captchawidth = {captchawidth}, captchaheight = {captchaheight}")
                    # 通过image处理图像，第二种方法：在整个可视区域截取
                    imgobject = Image.open('clawerimgs/screenshot.png')
                    imgcaptcha = imgobject.crop(
                        (captchax, captchay, captcharight, captchabottom))        # 裁剪
                    imgcaptcha.save('clawerimgs/captcha2.png')
'''


def captcha_recognition(*args, **kwargs):
    browser = args[0]
    veri_code_info = args[1]
    veri_code = ''
    global WM_LIBRARY_LIST
    cw_dir = SYS_PATCH  # os.getcwd()
    lib_file = veri_code_info["libfile"]
    wm_library_dict = None
    for wm_library in WM_LIBRARY_LIST:
        if wm_library["libfile"] == lib_file:
            wm_library_dict = wm_library
            break
    if not (wm_library_dict is None):
        lib_id = wm_library_dict["libid"]
    else:
        wm_library_dict = {"libfile": lib_file, "libid": -1}
        if lib_file[1] != ':':
            if lib_file[0] != '\\':
                lib_file = cw_dir + '\\' + lib_file
            else:
                lib_file = cw_dir + lib_file

        lib_password = WM_LIB_PASSWORD
        if veri_code_info.get("libpassword", '') != '':
            lib_password = veri_code_info["libpassword"]

        lib_id = load_wm_from_file_ex(lib_file, lib_password)
        options = veri_code_info["option"]
        for option in options:
            set_wm_option_ex(lib_id, option['index'], option['value'])

        wm_library_dict["libid"] = lib_id
        WM_LIBRARY_LIST.append(wm_library_dict)
    # 获取cookie信息
    # cookies = None  # browser.get_cookies()
    # 打印获取的cookies信息
    # print(cookies)
    # response = download_file(veri_code_info["url"], cookies)
    # if response.status_code == 200:
        # cookies = response.cookies.items()
        # print('回写cookies：', cookies)
        # if isinstance(cookies, list):
        #     for cookie in cookies:
        #         cookie_dict = {}
        #         cookie_dict['name'] = cookie[0]
        #         cookie_dict['value'] = cookie[1]
        #         browser.add_cookie(cookie_dict)
        # now_time = datetime.datetime.now()
        # now_time_str = now_time.strftime("%Y%m%d%H%M%S")
        # temp_dir = cw_dir + "\\temp\captcha"
        # if not os.path.exists(temp_dir):
        #     os.makedirs(temp_dir)
        # with open(temp_dir + "\\vcode_" + now_time_str + ".jpg", 'wb') as f:
        #     f.write(response.content)
        #     f.close()
        # b = response.content
        # veri_code = get_image_from_buffer_ex(lib_id, b)

    veri_code = get_image_from_file_ex(lib_id, veri_code_info['file_path'])
    print('验证码：', veri_code)
    if veri_code_info["calculator"]:
        veri_code = calculator(veri_code)
    return veri_code
    # print(vericode)


def open_web(web_info, after_open_func=None):
    result = ''
    # 实例化一个驱动类
    if web_info["webtype"] == 0:
        driver = webdriver.Ie()
    elif web_info["webtype"] == 1:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()
    driver.maximize_window()
    try:
        driver.implicitly_wait(30)
        driver.get(web_info["url"])
        driver.delete_all_cookies()
        cookie_list = web_info["cookies"]
        for cookie_dict in cookie_list:
            cookie_dict['path'] = cookie_dict['path'].replace('//', '/')
            driver.add_cookie(cookie_dict)
        driver.get(web_info["url"])
        # WebDriverWait(driver, 30).until(
        #     lambda driver: not (web_find_element(driver, web_info["fieldopensuccess"]) is None))
        if not (after_open_func is None):
            result = after_open_func(driver, web_info["data"])
    finally:
        driver.quit()
        return result


def operate_web(web_config, veri_code_func=None, after_logging_in_func=None, result_default=None):
    result = ''
    # 实例化一个驱动类
    if web_config["webtype"] == 0:
        driver = webdriver.Ie()
    elif web_config["webtype"] == 1:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()
    driver.maximize_window()
    # time.sleep(1)
    try:
        driver.implicitly_wait(30)
        # 打开谷歌浏览器
        driver.get(web_config["url"])
        while len(driver.get_cookies()) == 0:
            time.sleep(1)
            driver.get(web_config["url"])
        login_info = web_config["logininfo"]
        is_cookie_login = False
        if 'cookies' in login_info.keys():
            cookies = login_info['cookies']
            if len(cookies) > 0:
                for cookie_dict in cookies:
                    cookie_dict['path'] = cookie_dict['path'].replace('//', '/')
                    driver.add_cookie(cookie_dict)
                driver.get(web_config["url"])
                is_cookie_login = True
        if not is_cookie_login:
            vericode_info = None
            if 'vericodeinfo' in web_config.keys():
                vericode_info = web_config["vericodeinfo"]
            veri_code = ''
            n = 5
            while n > 0:
                n = n - 1
                if not (veri_code_func is None):
                    if not (vericode_info is None) and not (type(vericode_info) is str):
                        veri_code = veri_code_func(driver, vericode_info)
                web_auto_login(driver, login_info["userName"], login_info["passWord"], veri_code,
                               login_info["fieldusername"], login_info["fieldpassword"], login_info["fieldvericode"],
                               login_info["fieldsubmit"], login_info["javascript"])
                time.sleep(0.2)
                login_fail = web_find_element(driver, login_info["fieldloginfail"])
                if login_fail is None:
                    break
                else:
                    result = login_fail.text
                    if result.find("验证码") == -1:
                        break
                print("剩余循环执行次数:%s" % n)
        WebDriverWait(driver, 30).until(
            lambda driver: not (web_find_element(driver, login_info["fieldloginsuccess"]) is None))
        # print(driver.title)
        result = ''
        if not (after_logging_in_func is None):
            result = after_logging_in_func(driver, web_config["data"])
    finally:
        driver.quit()
        return result


def simulated_operate_web(web_config, after_logging_in_func=None, result_default=None):
    if result_default is None:
        result = {'rtCode': "9002", "rtMsg": "登录失败"}
    else:
        result = result_default
    # 实例化一个驱动类
    if web_config["webtype"] == 0:
        driver = webdriver.Ie()
    elif web_config["webtype"] == 1:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()
    driver.maximize_window()
    try:
        driver.implicitly_wait(30)
        # 打开谷歌浏览器
        timeout_count = 0
        driver.get(web_config["url"])
        while len(driver.get_cookies()) == 0:
            if timeout_count >= 5:
                result['rtCode'] = "9002"
                result['rtMsg'] = '登录失败，网报环境有问题，无法正常获取网报信息！'
                return result
            print('获取cookies为空')
            time.sleep(1)
            driver.get(web_config["url"])
            timeout_count += 1
        result['cookies'] = driver.get_cookies()
        login_info = web_config["logininfo"]
        template_file = SYS_PATCH + '/' + login_info['TemplateFile']
        is_logined = False
        if 'cookies' in login_info.keys():
            cookies = login_info['cookies']
            if len(cookies) > 0:
                for cookie_dict in cookies:
                    cookie_dict['path'] = cookie_dict['path'].replace('//', '/')
                    driver.add_cookie(cookie_dict)
                driver.get(web_config["url"])
                is_logined, chk_msg = execute_py_script_func(template_file, 'check_logined', driver, login_info)
        if not is_logined:
            vericode_info = None
            if 'vericodeinfo' in web_config.keys():
                vericode_info = web_config["vericodeinfo"]
            n = 5
            while n > 0:
                n -= 1
                if not (vericode_info is None) and not (type(vericode_info) is str):
                    if vericode_info.get('func_name', '') != '':
                        veri_code = execute_func(sys.modules[__name__], vericode_info['func_name'], driver,
                                                 vericode_info)
                        if veri_code is None:
                            continue
                        login_info['vericode'] = veri_code

                execute_result = execute_py_script_func(template_file, login_info['func_name'], driver, login_info)
                if type(execute_result) is str:
                    if execute_result[:8] == 'parsing:':
                        execute_result = parsing_operate_web(driver, driver, execute_result)

                if type(execute_result) is tuple:
                    # 返回结果值execute_result = (1, '提示信息') 1:登陆成功； 2：密码错误
                    if execute_result[0] == 0:
                        result['rtCode'] = "0000"
                    else:
                        result['rtCode'] = "9002"
                    result['rtMsg'] = execute_result[1]
                    if execute_result[0] in [0, 2]:
                        break
                else:
                    result['rtMsg'] = execute_result

                print(execute_result, "剩余循环执行次数:%s" % n)
            if execute_result[0] == 0:
                is_logined, chk_msg = execute_py_script_func(template_file, 'check_logined', driver, login_info)
                if is_logined:
                    cookies = execute_py_script_func(template_file, 'get_cookies', driver, login_info)
                    if cookies is None:
                        cookies = driver.get_cookies()

        if not is_logined:
            result['rtCode'] = "9002"
            result["cookies"] = []
        else:
            result["cookies"] = cookies
            result["url"] = driver.current_url
        result['rtMsg'] = chk_msg
        if is_logined and not (after_logging_in_func is None):
            result = after_logging_in_func(driver, web_config.get("data"), result)
    except Exception as e:
        print('[simulated_operate_web]异常错误：', e)
        # log_debug('异常报错：', e)
    finally:
        driver.quit()
        return result


def crop_web_img(browser, actionstr):
    imgframe = None
    # frame_x = 0
    # frame_y = 0
    frame_layer_count = 0
    try:
        frame_layer_count, curr_element = parsing_action(browser, browser, actionstr)
        # if frame_layer_count > 0:
        #     for curr_element in elements:
        #         if (str(type(curr_element)).find('WebElement') != -1) and curr_element.tag_name == 'iframe':
        # browser.switch_to.frame(curr_element)
        # curr_element = browser
        # frame_layer_count += 1
        # 先拿到iframe在整个可视页面（也就是上面的截屏）中的相对位置，因为前面对页面的窗口大小进行了设置960 x 960
        # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标
        # location 拿到的是相对整个html页面的坐标
        # frame_x = int(curr_element.location_once_scrolled_into_view['x'])
        # frame_y = int(curr_element.location_once_scrolled_into_view['y'])
        # else:
        #     curr_element = elements[-1]

        if (str(type(curr_element)).find('WebElement') != -1):
            curr_element.screenshot('veri_code.png')
            imgframe = Image.open('veri_code.png')
            '''
            # 截屏，在chrome中截取的是可视区域，而不是整个html页面
            browser.save_screenshot('screenshot.png')
            # 获取验证码x,y轴坐标
            location = curr_element.location
            # 获取验证码的长宽
            size = curr_element.size
            # 写成我们需要截取的位置坐标
            left = frame_x + int(location['x'])
            top = frame_y + int(location['y'])
            right = frame_x + int(location['x'] + size['width'])
            bottom = frame_y + int(location['y'] + size['height'])
            # 通过image处理图像，截取frame的图片 ———— 无意义，只是做经验总结
            imgframe = Image.open('screenshot.png')
            imgframe = imgframe.crop((left, top, right, bottom))  # 裁剪
            imgframe.save('verification_code.png'
            '''
    except Exception as e:
        print('[crop_web_img]异常错误：', e)
        # log_debug('异常报错：', e)
    finally:
        return_switch_to_frame(browser, frame_layer_count)
        return imgframe


def captcha_recognition_crop_img(*args, **kwargs):
    browser = args[0]
    veri_code_info = args[1]
    veri_code = ''
    global WM_LIBRARY_LIST
    cw_dir = SYS_PATCH  # os.getcwd()
    lib_file = veri_code_info["libfile"]
    wm_library_dict = None
    for wm_library in WM_LIBRARY_LIST:
        if wm_library["libfile"] == lib_file:
            wm_library_dict = wm_library
            break
    if not (wm_library_dict is None):
        lib_id = wm_library_dict["libid"]
    else:
        wm_library_dict = {"libfile": lib_file, "libid": -1}
        if lib_file[1] != ':':
            if lib_file[0] != '\\':
                lib_file = cw_dir + '\\' + lib_file
            else:
                lib_file = cw_dir + lib_file
        lib_password = veri_code_info["libpassword"]
        lib_id = load_wm_from_file_ex(lib_file, lib_password)
        options = veri_code_info["option"]
        for option in options:
            set_wm_option_ex(lib_id, option['index'], option['value'])

        wm_library_dict["libid"] = lib_id
        WM_LIBRARY_LIST.append(wm_library_dict)
    # 拷贝验证码图片
    script = veri_code_info["script"]
    img = crop_web_img(browser, script)
    if img is not None:
        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime("%Y%m%d%H%M%S")
        temp_dir = cw_dir + "\\temp\captcha"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        with open(temp_dir + "\\vcode_" + now_time_str + ".jpg", 'wb') as f:
            f.write(img.content)
            f.close()
        b = img.content
        veri_code = get_image_from_buffer_ex(lib_id, b)
        print('验证码：', veri_code)
        if veri_code_info["calculator"]:
            veri_code = calculator(veri_code)
    return veri_code
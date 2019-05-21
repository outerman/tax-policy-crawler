# coding=utf-8
# import random
import time
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from TaxPolicyCrawlerScrapy.util import Keymo
from TaxPolicyCrawlerScrapy.util import KeyDriverUtil
import win32api
import win32gui
import requests
import os


# 招商银行
class ZsyhRobot:
    browser = None

    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        iedriver = 'D:\shenxy\chromedriver\IEDriverServer.exe'  # iedriver路径
        os.environ["webdriver.ie.driver"] = iedriver  # 设置环境变量
        self.browser = webdriver.Ie(iedriver)

        # 登录界面
        self.browser.get('https://app.cmbchina.com/cevs/Login.aspx')

    # 对界面的异常提示做识别，如果由于某些原因出了弹出层，不继续、或点掉
    def check_load_exception(self):
        # iframe = self.browser.find_element_by_id('frmMain')

        # # 系统异常，啥也打不开—— 尊敬的用户：系统服务出现异常，请稍后再试。因此给您造成的不便，敬请谅解！(错误码C0117XJFE0XMY)
        # if self.browser.find_element_by_id('main-top').is_displayed() and iframe is None:
        #     return False
        #
        # # 打开界面，异常的提示框—— 登录失败！根据SessionId登录失败，错误原因：获取用户登录信息失败(错误码H0116MXEYP2KA)
        # if self.browser.find_element_by_id('layui-layer4').is_displayed():
        #     return False

        return True

    # 做尝试输入
    def fill_values(self):
        # 等待界面加载完
        WebDriverWait(self.browser, 20, 0.5).until(
            EC.visibility_of_element_located((By.ID, 'ctyList')))
        print("表单加载完成")

        # 1、找到登录框，进行输入
        self.browser.implicitly_wait(5)
        select_city = self.browser.find_element_by_id('ctyList')
        login_account = self.browser.find_element_by_id('LgCardId_Ctrl')
        login_pwd = self.browser.find_element_by_id('LgPasswd_Ctrl')
        catcha_input = self.browser.find_element_by_id('tbCaptcha')
        login_btn = self.browser.find_element_by_id('btnlogin')

        # 2、填写账号
        select_ctrl = Select(select_city)
        select_ctrl.select_by_value('0010')

        KeyDriverUtil.key_press(0x0f)
        # 110932257810501
        KeyDriverUtil.key_press(0x02)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x02)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x0b)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x0a)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x04)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x03)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x03)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x06)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x08)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x09)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x02)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x0b)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x06)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x0b)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x02)
        self.browser.implicitly_wait(0.5)

        KeyDriverUtil.key_press(0x0f)
        KeyDriverUtil.key_press(0x0f)
        # 574680
        KeyDriverUtil.key_press(0x06)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x08)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x05)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x07)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x09)
        self.browser.implicitly_wait(0.5)
        KeyDriverUtil.key_press(0x0b)
        self.browser.implicitly_wait(0.5)

        # 打验证码

        # 点击登录
        login_btn.click()

        # 解析数据，形成结构化json
        # return self.parse_bank_flow()


# 测试执行
robot = ZsyhRobot()
if robot.check_load_exception():
    print(robot.fill_values())

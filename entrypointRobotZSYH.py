# coding=utf-8
# import random
import datetime
import time

from selenium.webdriver import ActionChains
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
from TaxPolicyCrawlerScrapy.wm_code import web_operation


# 招商银行
from TaxPolicyCrawlerScrapy.wm_code.common import SYS_PATCH


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
        captcha_input = self.browser.find_element_by_id('tbCaptcha')
        login_btn = self.browser.find_element_by_id('btnlogin')

        # 2、填写账号
        

        n = 3
        while n > 0:
            # 打验证码
            captcha_path = save_captcha(self.browser, self.browser.find_element_by_id('imgCaptcha'))
            captcha = recognize_captcha(self.browser, captcha_path)
            print("本次验证码识别为：" + captcha)
            captcha_input.send_keys(captcha)

            # 点击登录
            login_btn.click()

            result = EC.alert_is_present()(self.browser)
            if result:
                if n == 0:
                    print(str(n) + "次都没有识别正确验证码，放弃了")
                    return
                n = n - 1
                result.accept()
            else:
                print("没有alert，验证码识别正确  ")
                break

        # 跳转到“对账单打印”
        self.browser.get('https://app.cmbchina.com/cevs/StatementMain.aspx')

        # 填写年月
        tyear = self.browser.find_element_by_id('tYear')
        tmonth = self.browser.find_element_by_id('tMonth')
        tyear.send_keys('2019')
        select_month = Select(tmonth)
        select_month.select_by_value('4')
        self.browser.find_element_by_id('Button1').click()

        # 解析数据，形成结构化json
        # return self.parse_bank_flow()
        bank_flow_result = trans_table_to_json(self.browser.find_element_by_id('vList'))

        print(bank_flow_result)

def recognize_captcha(browser, captcha_path):
    # img_url = browser.find_element_by_id('imgCaptcha').get_attribute('src')
    vericode_info = {
        # "url": img_url,
        "file_path": captcha_path,
        "libfile": "\TaxPolicyCrawlerScrapy\wm_code\data\zsyh.dat",
        "option": [{"index": 6, "value": 80}, {"index": 7, "value": -3}],
        "calculator": False,
        "libpassword": '123456'
    }
    return web_operation.captcha_recognition(browser, vericode_info)


def save_captcha(driver, element):
    action = ActionChains(driver).move_to_element(element)  # 移动到该元素
    action.context_click(element)  # 右键点击该元素
    action.send_keys(Keys.ARROW_DOWN)  # 点击键盘向下箭头
    action.send_keys('s')  # 键盘输入V保存图
    action.perform()  # 执行保存

    time.sleep(2)
    # driver.implicitly_wait(100)  # 等保存框弹出来
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y%m%d%H%M%S")
    temp_dir = SYS_PATCH + "\\temp\captcha" + "\\vcode_" + now_time_str + ".jpg"

    Keymo.press_paste(temp_dir)
    Keymo.press_alt_and('s')
    time.sleep(1)
    return temp_dir


def trans_table_to_json(table_bank_flow):
    result = []
    tr_list = table_bank_flow.find_elements_by_xpath(".//tbody//tr")
    for tr in tr_list:
        tr_ret = []
        td_list = tr.find_elements_by_xpath('.//td')
        for td in td_list:
            tr_ret.append(td.text)
        result.append(tr_ret)
    return result


# 测试执行
robot = ZsyhRobot()
if robot.check_load_exception():
    print(robot.fill_values())

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

from TaxPolicyCrawlerScrapy import settings
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
        self.user_agent_list = settings.USER_AGENTS
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

        self.browser.implicitly_wait(0.5)

        # 3、识别并填写验证码
        n = 5   # 最多尝试5次识别验证码
        while n > 0:
            # 打验证码
            captcha_path = save_captcha(self.browser, self.browser.find_element_by_id('imgCaptcha'))
            print("本地的验证码存储位置：" + captcha_path)
            captcha = recognize_captcha(self.browser, captcha_path)
            print("本次验证码识别为：" + captcha)
            # 先清空
            captcha_input.send_keys(Keys.CONTROL + 'a')
            captcha_input.send_keys(Keys.BACKSPACE)
            captcha_input.send_keys(captcha)

            # 4、点击登录
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

        # 5、跳转到“对账单打印”
        self.browser.get('https://app.cmbchina.com/cevs/StatementMain.aspx')

        # TODO 可以尝试通过requests请求“https://app.cmbchina.com/cevs/StatementMain.aspx”带上cookies，来请求，而不是界面点击
        # 6、填写年月
        tyear = self.browser.find_element_by_id('tYear')
        tmonth = self.browser.find_element_by_id('tMonth')
        tyear.send_keys('2019')
        select_month = Select(tmonth)
        select_month.select_by_value('4')
        self.browser.find_element_by_id('Button1').click()

        # 7、解析数据，形成结构化json
        # return self.parse_bank_flow()
        bank_flow_result = trans_table_to_json(self.browser.find_element_by_id('vList'))

        print(bank_flow_result)


def recognize_captcha(browser, captcha_path):
    # Private Declare Function SetWmOption Lib "WmCode.dll" (ByVal OptionIndex As Long,ByVal OptionValue As Long) As Boolean
    # 函数功能说明：设定识别库选项。设定成功返回真，否则返回假。
    # 函数参数说明：
    # OptionIndex ：整数型，选项索引，取值范围1〜7
    # OptionValue ：整数型，选项数值。
    #
    # 参数详解：
    # 	OptionIndex	OptionValue
    # 1.返回方式	取值范围：0〜1     默认为0,直接返回验证码,为1返回验证码字符和矩形范围形如：S,10,11,12,13|A,1,2,3,4 表示识别到文本 S 左边横坐标10,左边纵坐标11,右边横坐标,右边纵坐标12
    # 2.识别方式    取值范围：0〜4     默认为0,0整体识别,1连通分割识别,2纵分割识别,3横分割识别,4横纵分割识别。可以进行分割的验证码，建议优先使用分割识别，因为分割后不仅能提高识别率，而且还能提高识别速度
    # 3.识别模式	取值范围：0〜1     默认为0,0识图模式,1为识字模式。识图模式指的是背景白色视为透明不进行对比，识字模式指的是白色不视为透明，也加入对比。绝大多数我们都是使用识图模式，但是有少数部分验证码，使用识字模式更佳。
    # 4.识别加速	取值范围：0〜1     默认为0,0为不加速,1为使用加速。一般我们建议开启加速功能，开启后对识别率几乎不影响。而且能提高3-5倍识别速度。
    # 5.加速返回	取值范围：0〜1     默认为0,0为不加速返回,1为使用加速返回。使用加速返回一般用在粗体字识别的时候，可以大大提高识别速度，但是使用后，会稍微影响识别率。识别率有所下降。一般不是粗体字比较耗时的验证码，一般不用开启
    # 6.最小相似度	取值范围：0〜100   默认为90
    # 7.字符间隙    取值范围：-10〜0   默认为0,如果字符重叠,根据实际情况填写,如-3允许重叠3像素,如果不重叠的话,直接写0，注意：重叠和粘连概念不一样，粘连的话，其实字符间隙为0.

    captcha_length = 4   # 固定验证码长度4
    vericode_info = {
        # "url": img_url,
        "file_path": captcha_path,
        "libfile": "\TaxPolicyCrawlerScrapy\wm_code\data\zsyh.dat",
        "option": [{"index": 2, "value": 2}, {"index": 6, "value": 80}, {"index": 7, "value": 3}],
        "calculator": False,
        "libpassword": '123456'
    }
    tmp_captcha = web_operation.captcha_recognition(browser, vericode_info)

    return (tmp_captcha + "1111")[0:captcha_length]   # 如果不足4位，补足4位


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

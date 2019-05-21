import random
import time
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from TaxPolicyCrawlerScrapy.util import Keymo
from TaxPolicyCrawlerScrapy.util import KeyDriverUtil
import win32api
import win32gui
import requests


# 浦发银行
class PfyhRobot:
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
        self.browser = webdriver.Chrome("D:\shenxy\chromedriver\chromedriver-2.exe")

        # 登录界面
        self.browser.get('https://ebank.spdb.com.cn/newent/gb/login/prof.jsp')

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
        # # 切换到待操作的iframe里
        # self.browser.switch_to.frame('frmMain')
        # self.browser.switch_to.frame('frmSheet')

        # 等待界面加载完，弹出UKEY的框
        WebDriverWait(self.browser, 20, 0.5).until(
            EC.invisibility_of_element_located((By.ID, 'modal-confirm')))
        print("表单加载完成")

        # 0、UKEY弹出框确认
        self.browser.implicitly_wait(5)
        ukey_confirm = self.browser.find_element_by_id('modal-confirm')
        ukey_confirm.click()

        # 1、找到登录框，进行输入
        self.browser.implicitly_wait(5)
        login_box = self.browser.find_elements_by_xpath('//div[@class="login-box"]')[0]
        org_num = login_box.find_elements_by_xpath('.//div')[0].find_element_by_id('CifNo')
        login_name = login_box.find_elements_by_xpath('.//div')[1].find_element_by_id('LoginId2')
        password = login_box.find_element_by_id('OPassword')
        login_btn = login_box.find_elements_by_xpath('.//div')[3].find_element_by_tag_name('input')

        login_name.send_keys('qd01')
        # password.send_keys('112233')
        # Keymo.press_key('1')
        # Keymo.press_key('1')
        # Keymo.press_key('2')
        # Keymo.press_key('2')
        # Keymo.press_key('3')
        # Keymo.press_key('3')
        password.click()
        # Keymo.keyboard.press_key('1')
        # Keymo.keyboard.release_key('1')
        KeyDriverUtil.key_press(0x02)
        self.browser.implicitly_wait(1)
        KeyDriverUtil.key_press(0x02)
        self.browser.implicitly_wait(1)
        KeyDriverUtil.key_press(0x03)
        self.browser.implicitly_wait(1)
        KeyDriverUtil.key_press(0x03)
        self.browser.implicitly_wait(1)
        KeyDriverUtil.key_press(0x04)
        self.browser.implicitly_wait(1)
        KeyDriverUtil.key_press(0x04)
        self.browser.implicitly_wait(1)

        # 点击“登录”，弹出ukey的密码输入框
        # Keymo.click_screen(login_btn.location.get())
        # login_btn.submit()
        # login_btn.click()
        # self.browser.execute_async_script('doSubmit()')
        # handle = self.browser.current_window_handle
        Keymo.click(win32gui.GetForegroundWindow(), login_btn.location.get('x') + 100, login_btn.location.get('y') + 180)

        # # 输入ukey的pin码，先等待pin码输入框出来
        # self.browser.implicitly_wait(5)
        # KeyDriverUtil.key_press(0x02)
        # self.browser.implicitly_wait(1)
        # KeyDriverUtil.key_press(0x02)
        # self.browser.implicitly_wait(1)
        # KeyDriverUtil.key_press(0x03)
        # self.browser.implicitly_wait(1)
        # KeyDriverUtil.key_press(0x03)
        # self.browser.implicitly_wait(1)
        # KeyDriverUtil.key_press(0x04)
        # self.browser.implicitly_wait(1)
        # KeyDriverUtil.key_press(0x04)
        # self.browser.implicitly_wait(1)
        #
        # # 提交pin码
        # KeyDriverUtil.key_press(0x1c)

        # 切换到历史查询
        self.browser.get('https://ebank.spdb.com.cn/newent/main?transName=PreQueryHistory')

        # 查询交易历史记录
        self.get_bank_flow_by_ui()
        # self.get_bank_flow()

        # 解析数据，形成结构化json
        return self.parse_bank_flow()

    # 通过模拟界面输入和点击的方式来查询
    def get_bank_flow_by_ui(self):
        begin_date = self.browser.find_element_by_id('BeginDate')
        end_date = self.browser.find_element_by_id('EndDate')
        btn_query = self.browser.find_element_by_name('submitquery ')

        begin_date.send_keys(Keys.CONTROL + 'a')
        begin_date.send_keys(Keys.BACKSPACE)
        begin_date.send_keys('20190510')
        end_date.send_keys(Keys.CONTROL + 'a')
        end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys('20190519')
        btn_query.click()

    # 通过发送请求的方式来查询，暂未成功（ajax请求，并且返回的是jsp页面，可能需要执行js脚本？）
    def get_bank_flow(self):
        session = requests.session()
        # session.verify = False
        session.get('https://databank.spdb.com.cn/etrack/?master_id=2016585655&user_mark=2016585655qd01&channel=83&page_tag=%2Fgb%2Fbasic%2FQueryHistoryEBillRes.jsp&session_id=HrTSvklA_8wJL5Y9BQeu_1trrfTyrZwchLFXnLoegPaQCZ5S9COe!-2011606763!1558313847104&event=click&event_type=INPUT&event_value=%E6%9F%A5%E8%AF%A2&data=%7B%22contentWidth%22%3A809%2C%22contentHeight%22%3A596%2C%22offsetX%22%3A1011.0625%2C%22offsetY%22%3A193%2C%22xpath%22%3A%22%2FHTML%2FBODY%2FDIV%2FFORM%2FTABLE%2FTBODY%2FTR%2FTD%5B4%5D%2FINPUT%22%2C%22referrer%22%3A%22https%3A%2F%2Febank.spdb.com.cn%2Fnewent%2Fmain%22%2C%22auto_flag%22%3Atrue%7D&time=2019-04-20%2009%3A02%3A32%3A338&url=https%3A%2F%2Febank.spdb.com.cn%2Fnewent%2Fmain&browser_lang=zh-CN&browser_name=Chrome&browser_version=74.0.3729.157&os=Windows10&random=0.07658639261061273')

        # session.get('https://ebank.spdb.com.cn/')
        ua_headers = {'User-Agent': random.choice(self.user_agent_list)}
        session.headers.update(ua_headers)
        session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'})
        # session.headers.update({'Cookie':'SPDB_ENT_SESSIONID=nV7KB6EC6-j1mfFeVKDVtOVSOhnxDFhCNWnLJnXrHohcMgGkWa5R!-806585956; spdb_login_spdb=LoginType:2'})
        session.headers.update({'Cookie': 'SPDB_ENT_SESSIONID=' + self.browser.get_cookie('SPDB_ENT_SESSIONID')['value'] + '; spdb_login_spdb=' + self.browser.get_cookie('spdb_login_spdb')['value']})
        resp = session.post('https://ebank.spdb.com.cn/newent/main', 'transName=QueryHistory&SeqNo=&AcctNo=91450078801600000266&BeginDate=20190510&EndDate=20190519&TxAmount=&PayeeAcctNo=&Payee=&BeginNumber=1&QueryNumber=30&TotalPage=1&QueryPage=')
        print(resp.content)

    def parse_bank_flow(self):
        form_bank_flow = self.browser.find_element_by_id('form1')
        table_bank_flow = form_bank_flow.find_element_by_xpath('.//table[@class="table2 table1"]')
        return trans_table_to_json(table_bank_flow)


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
robot = PfyhRobot()
if robot.check_load_exception():
    print(robot.fill_values())

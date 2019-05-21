import time
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DzsjRobot:
    browser = None

    def __init__(self):
        self.browser = webdriver.Chrome("/Users/shenxy/Documents/work/tech/Github/InvoiceCrawlerScrapy/chromedriver/mac"
                                        "/chromedriver")

        # 此处的链接是网上电厅的链接，在已登录状态下，打开即可进行录入
        self.browser.get(
            'http://gdcsgj.test.jchl.com/sbzs-cjpt-web/biz/sbzs/ybnsrzzs?gdslxDm=1&bzz=csgj&sssqQ=2018-12-01&sssqZ'
            '=2018-12-31&token=FF808081667BA9CC016855D4EA40088D&nsrsbh=914413023232962997&acctid=0000078&userid'
            '=2000001144&username=xyf&gsnsrsbh=914413023232962997&dsnsrsbh=914413023232962997&sign'
            '=d9bef871178559299f9346e14b6c91a0&yypt_nsrsbh=914413023232962997&swjgDm=14413020000&identify'
            '=EDD7D4E07F00000140FD65789E230400&permissionID=101005&sfxssp=false&gzsb=Y')

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
        # 切换到待操作的iframe里
        self.browser.switch_to.frame('frmMain')
        self.browser.switch_to.frame('frmSheet')

        # 等待界面加载完
        WebDriverWait(self.browser, 20, 0.5).until(
            EC.invisibility_of_element_located((By.ID, 'marqueeFrmSheet')))
        print("表单加载完成")

        # 1、找到单元格，进行输入
        self.browser.implicitly_wait(5)
        table1 = self.browser.find_elements_by_xpath('//div[@class="NewTableMain"]//table')[1]
        tr1 = table1.find_elements_by_xpath('.//tbody//tr')[3]
        tr_default = table1.find_elements_by_xpath('.//tbody//tr')[0]
        td1 = tr1.find_elements_by_xpath('.//td[@class="edit right"]')[0]
        input_cell = td1.find_element_by_xpath('.//input')
        input_cell.click()
        input_cell.clear()
        input_cell.send_keys("123.00")
        # 移除焦点，使程序执行校验等逻辑
        tr_default.click()

        # 2、同一行，下一个输入框
        td1 = tr1.find_elements_by_xpath('.//td[@class="edit right"]')[1]
        input_cell = td1.find_element_by_xpath('.//input')
        input_cell.click()
        input_cell.clear()
        input_cell.send_keys("234.54")
        # 移除焦点，使程序执行校验等逻辑
        tr_default.click()

        # 3、换一行，下一个输入框
        time.sleep(0.5)     # 此处需要稍作等待，否则报错，可能和selenium的运行机制有关系
        tr1 = table1.find_elements_by_xpath('.//tbody//tr')[4]
        td1 = tr1.find_elements_by_xpath('.//td[@class="edit right"]')[0]
        input_cell = td1.find_element_by_xpath('.//input')
        input_cell.click()
        input_cell.clear()
        input_cell.send_keys("567.34")
        # 移除焦点，使程序执行校验等逻辑
        tr_default.click()

        # 4、换一行，下一个输入框
        td1 = tr1.find_elements_by_xpath('.//td[@class="edit right"]')[1]
        input_cell = td1.find_element_by_xpath('.//input')
        input_cell.click()
        input_cell.clear()
        input_cell.send_keys("890.12")
        # 移除焦点，使程序执行校验等逻辑
        tr_default.click()

        # 返回到默认dom树最外层
        self.browser.switch_to.default_content()

# 测试执行
robot = DzsjRobot()
if robot.check_load_exception():
    robot.fill_values()

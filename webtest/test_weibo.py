# -*- coding:utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture(scope="class")
def driver_init(request):
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(15)
    driver.maximize_window()
    driver.get("https://weibo.com/")
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("driver_init")
class TestSina:
    def __init__(self):
        self.username = "your account"
        self.password = "your password"
    def login(self, username, password):
        elem_user = self.driver.find_element("id", "loginname")
        elem_user.clear()
        elem_user.send_keys(username)
        elem_pwd = self.driver.find_element("name", "password")
        elem_pwd.clear()
        elem_pwd.send_keys(password)
        elem_pwd.send_keys(Keys.RETURN)
        time.sleep(5)
        assert "我的收藏" in self.driver.page_source, "登录失败！"

    def logout(self):
        self.driver.find_element("css selector", "a>em[class='W_ficon ficon_set S_ficon']").click()
        self.driver.find_element("css selector", "li[class='gn_func']").click()
        time.sleep(2)
        assert "我的主页" not in self.driver.page_source, "退出失败！"

    def test_search(self):
        self.login(self.username, self.password)
        elem_search = self.driver.find_element("css selector", "div>input[node-type='searchInput']")
        elem_search.clear()
        search_content = "南京航空航天大学"
        elem_search.send_keys(search_content)
        time.sleep(1)
        elem_search.send_keys(Keys.RETURN)
        time.sleep(2)
        assert "微博搜索" in self.driver.page_source and search_content in self.driver.page_source, "搜索失败！"
        self.driver.find_element("class name", "avator").click()
        assert "关注" in self.driver.page_source, "无法打开微博主页"
        self.logout()

    def test_fabu(self):
        self.login(self.username, self.password)
        elem_fabu = self.driver.find_element("css selector", "textarea.W_input")
        for i in range(5):
            elem_fabu.send_keys(f"hello weibo! for test:{i}")
            time.sleep(2)
            self.driver.find_element("css selector", "a.W_btn_a:nth-child(2)").click()
            time.sleep(2)
            assert "发布成功" in self.driver.page_source, f"发布第{i+1}条微博失败！"
        self.logout()

    def test_delete(self):
        self.login(self.username, self.password)
        self.driver.find_element("css selector", "div>a[bpfilter='page_frame']").click()
        for i in range(5):
            time.sleep(3)
            self.driver.find_element("css selector", "div>a[action-type='fl_menu']").click()
            time.sleep(2)
            self.driver.find_element("css selector", "li>a[action-type='feed_list_delete']").click()
            time.sleep(2)
            self.driver.find_element("css selector", "p>a[class='W_btn_a']").click()
            time.sleep(2)
        self.logout()

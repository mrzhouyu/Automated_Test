# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 18:39
# @Author  : YuChou
# @Site    : 
# @File    : Download.py
# @Software: PyCharm
from selenium import webdriver
import requests
driver=webdriver.Chrome()


class Download():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.User_Agent={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

    def login_and_return_cookies(self):
        driver=self.driver
        driver.get(
            "http://10.230.0.41:9080/login?from=%2Fblue%2Forganizations%2Fjenkins%2FSmartRetail2%2Fdetail%2FSmartRetail2%2F58%2Fartifacts")
        # self.driver.implicitly_wait(5)
        driver.find_element_by_id("j_username").click()
        driver.find_element_by_id("j_username").clear()
        driver.find_element_by_id("j_username").send_keys("zhouyu")
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("zhouyu!321")
        driver.find_element_by_id("yui-gen1-button").click()
        driver.get_cookies()

    def get_conten(self,cookies,times=0):
        try:
            print("执行到这里了")
            print(cookies)
            req=requests.post("http://10.230.0.41:9080/blue/organizations/jenkins/SmartRetail2/detail/SmartRetail2/58/artifacts/",cookies=cookies,headers=self.User_Agent)
            req.encoding=req.apparent_encoding
            if req.status_code==200:
                return req.text
            else:
                if times<3:
                    self.get_conten(cookies,times=times+1)
                else:
                    print('多次尝试连接未成功！')
        except:
            print("connections error!")



    def downzip(self):
        pass


if __name__ == '__main__':
    down=Download()
    cookies=down.login_and_return_cookies()
    down.get_conten(cookies)

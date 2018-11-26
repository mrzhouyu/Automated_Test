# -*- coding: utf-8 -*-
# @Time    : 2018/9/26 14:58
# @Author  : YuChou
# @Site    :
# @File    : locusettest1.py
# @Software: PyCharm

from locust import HttpLocust,TaskSet,task

class test_126(TaskSet):
    @task
    def test_baidu(self):
        header = {
            "User-Agent": "Mozilla/5.0 "  
                          "(Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "      
                          "(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
        r=self.client.get("http://10.230.2.36/",timeout=30,headers=header)
        assert r.status_code==200

class websiteUser(HttpLocust):
    task_set = test_126
    min_wait = 3000
    max_wait = 6000



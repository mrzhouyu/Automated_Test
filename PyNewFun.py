# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 9:37
# @Author  : YuChou
# @Site    : 
# @File    : PyNewFun.py
# @Software: PyCharm
import requests
import urllib3
url="http://10.230.2.36/share/test_case_2.py"
r=requests.get(url)
with open("dow.py",'wb') as f:
    f.write(r.content)
# def out():
#     for i in [1,2,3,4,5,6,7]:
#         if i>3:
#             yield i
#         print(i)
#
# x=out()
# print(next(x))
# print(x.__next__())
# print(x.__next__())
# print(x.__next__())
# for i in x:
#     print(i)




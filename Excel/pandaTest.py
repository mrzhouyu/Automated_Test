# -*- coding: utf-8 -*-
# @Time    : 2018/11/24 17:47
# @Author  : YuChou
# @Site    : 
# @File    : pandaTest.py
# @Software: PyCharm
import pandas as pd

datas = pd.read_csv("log.csv", header=0, encoding="utf8")

print(datas.head(0))
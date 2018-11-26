# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 17:05
# @Author  : YuChou
# @Site    :
# @File    : conf.py
# @Software: PyCharm

import re
import time
start=time.time()
time.sleep(2)
end=time.time()
t=time.asctime(time.localtime(end-start))
print(t)
print(re.findall('(:\d{2}:\d{2})',t)[0].strip(':'))



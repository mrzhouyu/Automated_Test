# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 21:49
# @Author  : YuChou
# @Site    : 
# @File    : test.py
# @Software: PyCharm
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
fig=plt.figure(figsize=(8,6),dpi=80)
fig.suptitle("ceshitu")
plt.subplot(1,2,1)
plt.xlim(1,5)
plt.ylim(1,5)
plt.xlabel("x轴")
plt.ylabel("y轴")
plt.xticks([0,0.1,0.2,0.3,0.6,1,1.5,2,2.8,3])
plt.plot([1,2,3],[1,2,3],color="red",linestyle="--",label="hello")
plt.legend(loc="upper left")
plt.subplot(1,2,2)
plt.plot([1,2,3],[4,5,6])
plt.show()

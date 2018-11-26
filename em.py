# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 13:55
# @Author  : YuChou
# @Site    : 
# @File    : em.py
# @Software: PyCharm
import re
from collections import Counter
def cal(path):
    number_dic={}
    with open(path,'r') as f:
        while True:
            datas=f.readline()
            if datas !='':
                data=re.findall(r"\[.*\]",datas)[0]
                data_list=re.findall('\d{1,4}',data)
                for i in data_list:
                    if i in number_dic.keys():
                        number_dic[i]+=1
                    else:
                        number_dic[i]=1
            else:
                break
    print(number_dic)
def test():
    l= [0,1,2,3,4,5]
    for i ,c in enumerate(l):
        print(i)
        print(c)
if __name__=="__main__":
    # cal("E:\PythonPrJ\Automated_Test\datas.txt")
    test()
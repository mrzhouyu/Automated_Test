# -*- coding: utf-8 -*-
# @Time    : 2018/11/5 10:09
# @Author  : YuChou
# @Site    :
# @File    : test2.py
# @Software: PyCharm
import pymongo
from matplotlib import pyplot as plt
import numpy as np
import re
def getCollection():
    try:
        con = pymongo.MongoClient("mongodb://zhouyu:915603@10.230.2.36:27017")
        db = con.huojia
        coll = db.datas
        return coll
    except:
        print("error")

def outData():
    con=getCollection()
    d=con.find()
    #所有集合数据
    allCo=[]
    for c in d:
        allCo.append(c)
    return allCo


def plotALL():
    plt.figure()
    d=outData()
    keyTop=[]
    for k in d.keys():
        keyTop.append(k)
    keyTop=keyTop[1:]#所有的层高


    for local,p in enumerate(keyTop):
        keyMiddele = []
        if local+1==1:
            plt.subplot(2,4,local+1)
        if local+1==2:
            plt.subplot(2,4,3)
        if local+1==3:
            plt.subplot(2,4,5)
        if local+1==4:
            plt.subplot(2,4,7)
        if local+1==5:
            plt.subplot(2,4,2)
        if local+1==6:
            plt.subplot(2,4,4)
        if local+1==7:
            plt.subplot(2,4,6)
        if local+1==8:
            plt.subplot(2,4,8)

        for k in d[p]:
            keyMiddele.append(int(k))
        keyMiddele=sorted(keyMiddele)#0~17排序

        for i in keyMiddele:
            c=d[p][str(i)]
            for j in c.keys():
                height=int(j)
                s=c[j]
                if s<20:
                    continue
                plt.scatter(i,height,s=3,alpha=0.5)
        plt.title(p,color="blue")
        plt.xlim(0,17)
        plt.xticks(range(0,18))
        jugle=re.findall(r"(\d{1,3})",p)[0]
        yMaxSize=(int(jugle)//10+1)*10+4
        yMinSize=(int(jugle)//10)*10-4
        plt.ylim(yMinSize,yMaxSize)
    plt.savefig("盖片对比.jpg", dpi = 300)
    # plt.show()

plotALL()
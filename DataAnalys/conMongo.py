# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 13:27
# @Author  : YuChou
# @Site    : 
# @File    : conMongo.py
# @Software: PyCharm
import pymongo
import json

def getCollection():
    try:
        con = pymongo.MongoClient("mongodb://zhouyu:915603@10.230.2.36:27017")
        db = con.huojia
        coll = db.datas
        return coll
    except:
        print("error")

def loadsJsonAB(s=getCollection()):
    with open("allAB.json",'r') as f:
        results=json.load(f)
        s.insert(results)

def loadsJsonCD(s=getCollection()):
    with open("allCD.json",'r') as f:
        results=json.load(f)
        s.insert(results)

if __name__=="__main__":
    loadsJsonAB()
    loadsJsonCD()

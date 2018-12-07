# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 10:09
# @Author  : YuChou
# @Site    : 
# @File    : DataQuery.py
# @Software: PyCharm
import pymongo
import re
import sys
HOST = "localhost"
PORT = 27017
DATABASE = "syslog"




class MonCom():

    def __init__(self):
        self.client = pymongo.MongoClient(HOST, PORT)
        self.db = self.client[DATABASE]
        self.Stime, self.Etime = self.getArg()


    # 输入参数验证是否正确
    def argCheck(self, argList):
        s = " ".join(argList)
        checkResult = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} \d{4}-\d{2}-\d{2} \d{2}:\d{2}", s)
        if checkResult:
            return "".join(argList[:2]), " ".join(argList[2:])
        else:
            return False

    # 获取输入参数
    def getArg(self):

        if len(sys.argv) != 5:
            print("err 输入参数不够")
            print("usage example: 2000-01-01 01:01 2000-01-01 01:02")
            sys.exit(1)

        elif self.argCheck(sys.argv[1:]) == False:
            print("err 没有正确的输入参数")
            print("usage example: 2000-01-01 01:01 2000-01-01 01:02")
            sys.exit(1)
        else:
            return self.argCheck(sys.argv[1:])


    def queryEvent(self):
        pass
    def invalidTof(self):
        cmd = '{message:/Invalid tof event/,"timestamp":{$gt:"'+self.Stime+'",$lt:"'+self.Etime+'"}}'
        count = self.db["run"].find(cmd).count()
        return count

    def invalidWeight(self):
        cmd = '{message:/Invalid weight event/,"timestamp":{$gt:"'+self.Stime+'",$lt:"'+self.Etime+'"}}'
        count = self.db["run"].find(cmd).count()
        return count

if __name__=="__main__":
    M = MonCom()

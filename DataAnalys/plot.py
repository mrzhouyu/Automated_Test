# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 21:48
# @Author  : YuChou
# @Site    : 
# @File    : plot.py
# @Software: PyCharm
import re
import pandas
import json
import numpy
import os
import pymongo

# PATHList=os.listdir(os.getcwd()+"\\"+os.listdir(os.getcwd())[0])





class DataAn():
    def __init__(self):
        self.fileList = [os.path.join(root,file) for root,dir,files in os.walk(os.getcwd()) for file in files if "log" in file ]
        self.dataDic = self.getDatas()
    #
    #
    def getDatas(self):
        dataTreeAB={}
        dataTreeCD={}
        for path in self.fileList:
            if "A" in path.split("\\")[-1] or "B" in path.split("\\")[-1] :
                print(path)
                with open(path,"r",encoding="utf8") as f:
                    sDic={}
                    lines=f.readlines()
                    for line in lines:
                        channelAndRange=re.findall(r"channel (\d{1,2}), range (\d{1,3})",line)
                        if channelAndRange != []:
                            if channelAndRange[0][0] not in sDic.keys():
                                sDic[channelAndRange[0][0]]={channelAndRange[0][1]:1}
                            elif channelAndRange[0][1] not in sDic[channelAndRange[0][0]].keys():
                                sDic[channelAndRange[0][0]][channelAndRange[0][1]]=1
                            else:
                                sDic[channelAndRange[0][0]][channelAndRange[0][1]]+=1
                dataTreeAB[path.split("\\")[-1].split(".")[0]]=sDic

            elif "C" in path.split("\\")[-1] or "D" in path.split("\\")[-1]:
                with open(path,"r",encoding="utf8") as f:
                    sDic={}
                    lines=f.readlines()
                    for line in lines:
                        channelAndRange=re.findall(r"channel (\d{1,2}), range (\d{1,3})",line)
                        if channelAndRange != []:
                            if channelAndRange[0][0] not in sDic.keys():
                                sDic[channelAndRange[0][0]]={channelAndRange[0][1]:1}
                            elif channelAndRange[0][1] not in sDic[channelAndRange[0][0]].keys():
                                sDic[channelAndRange[0][0]][channelAndRange[0][1]]=1
                            else:
                                sDic[channelAndRange[0][0]][channelAndRange[0][1]]+=1
                dataTreeCD[path.split("\\")[-1].split(".")[0]]=sDic
            else:
                break

        return dataTreeAB,dataTreeCD

    def saveJsonAB(self):
        with open("allAB.json","w") as j:
            print(len(self.dataDic))
            json.dump(self.dataDic[0],j)

    def saveJsonCD(self):
        with open("allCD.json",'w') as j:
            json.dump(self.dataDic[1],j)

    def saveAlhl(self):
        self.saveJsonAB()
        self.saveJsonCD()
class Plot():

    def __init__(self):
        self.api=self.conData()

    def conData(self):
        try:
            con = pymongo.MongoClient("mongodb://zhouyu:915603@10.230.2.36:27017")
            db = con.huojia
            coll = db.datas
            return coll
        except:
            print("error")
    def getDatas(self):
        datas=self.api.find()
        for data in datas:
            print(data)
    def plot(self):
        pass
if __name__=="__main__":
    p=Plot()
    p.getDatas()


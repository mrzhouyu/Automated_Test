# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 12:36
# @Author  : YuChou
# @Site    : 
# @File    : QueryDeri.py
# @Software: PyCharm
import csv
import os
import re
#更改文件名字
def reName():
    path = "E://scripts//4//pick-up-sku//"
    csvList = os.listdir(path)
    for csv in csvList:
        l = csv.split('-')
        l[7] = "400" + l[7]
        newName = path + "-".join(l)
        oldName = path + csv
        os.rename(oldName, newName)
# reName()
#比较两个文件是否一致
def compileFile():
    erpPath="E://4//log.csv//log.csv"
    csvPath="E://4//pick-up-sku//"
    notExist=[]
    csvCaseList=[]
    for line in os.listdir(csvPath):
        csvCaseList.append(line.split('-')[7])
    with open(erpPath,"r",encoding="utf8") as f:
        reads=csv.reader(f)
        rows=[row for row in reads]
        for j in rows[1:]:
            if j[0] not in csvCaseList:
                notExist.append(j[0])
        print("下列csv文件无法在log里找到ERP: ",end="")
        print(notExist)
    return csvCaseList
def reLog():
    newData=[]


    with open("E://scripts//4//log.csv//log1.csv", "w", encoding="utf8") as k:
        writer = csv.writer(k)
        with open("E://scripts//4//log.csv//log.csv", "r", encoding="utf8") as f:
            reads = csv.reader(f)
            rows = [row for row in reads]
            newData.append(tuple(rows[0]))
            for j in rows[1:]:
                j[0] = "400" + j[0]
                print(j)
                writer.writerow(j)

reLog()


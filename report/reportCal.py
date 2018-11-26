# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 13:48
# @Author  : YuChou
# @Site    : 
# @File    : reportCal.py
# @Software: PyCharm
import os
import sys
import re
import csv
import time

class Report():

    def __init__(self):
        self.ConfEnv()
        self.filterTime = self.getArg() #判断命令行输入过滤是否正确 返回正确的过滤字段
        self.executeReport() #执行report程序 生成log下所有日志
        self.mergeCsv() #生成文件

    def ConfEnv(self):
        os.system('cat /etc/profile | awk "/export .*PATH=/{print }"  > /opt/bin/p.sh')
        os.system("bash p.sh")

    def executeReport(self):
        fileList = os.listdir(".")
        if "report" not in fileList:
            print("该目录下没有report程序，请确保本程序所在目录正确")
            sys.exit(1)
        elif "log" not in fileList:
            print("该目录下没有log的文件夹，请确保本程序所在目录正确")
            sys.exit(1)
        else:
            cmd = "./report " + self.filterTime
            print("正在输入执行shell脚本命令："+cmd)
            status = os.system(cmd)

            if status !=0 :
                print("report执行出错,返回非零状态码,结束主程序！")
                sys.exit(1)
        return None
    #输入参数验证是否正确
    def argCheck(self, argList):
        s = " ".join(argList)
        checkResult = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} \d{4}-\d{2}-\d{2} \d{2}:\d{2}",s)
        if checkResult:
            return s
        else:
            return False

    #获取输入参数
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


    def mergeCsv(self):
        CreatedDir = re.sub(" ","_",re.sub(":", "_", self.filterTime))
        os.chdir("log")
        os.chdir(CreatedDir)
        allList = [] #解析的总体数据
        logFile = ["detail_cpu.csv", "detail_disk.csv", "detail_memory.csv", "detail_proc.csv", "detail_reboot.csv", "detail_sku.csv", "detail_stable.csv", "tofConflict.csv"]
        for n, file in enumerate(logFile):
            with open(file, 'r', encoding="utf-8") as f:
                readDatas = csv.reader(f)
                if n == 0:
                    for item in readDatas:
                        allList.append(item)
                else:
                    for i, item in enumerate(readDatas):
                        allList[i]=allList[i]+item[4:]

        self.writeCsv(allList) #存储合并CSV数据 并且返回画图函数工作路径


    #创造当前时间的log路径存入log，且利用闭包返回该路径 供后面画图函数调用
    def writeCsv(self, datas):
        datas = self.sortUp(datas)
        os.chdir("..")  #注释掉此行 该文件生成在 2018-。。。文件夹下
        # csvFile = open(self.filterTime.replace(":","")+".csv","a", encoding="utf8", newline='') #生产模式用
        csvFile = open("Testlog.csv","w", encoding="utf8", newline='')

        writer = csv.writer(csvFile)
        for data in datas:
            writer.writerow(data)
        csvFile.close()

    #按照顺序过滤
    def sortUp(self,d):
        grade = 0
        copyDatas = []
        filterDic = {}
        for index ,data in enumerate(d):
            if index == 0:
                continue
            if data[4].strip() != '0':
                grade += 5
            if data[5].strip() != '0':
                grade+=5
            if data[6].strip() != '0':
                grade += 5
            if data[7].strip() != '0':
                grade += 10
            if data[8].strip() != '0':
                grade += 10
            if data[11].strip() != '0':
                grade += 10
            if data[13].strip() != '0':
                grade += 10
            filterDic[index] = grade
            grade = 0
        values = list(filterDic.values())
        values = sorted(values, reverse=True)

        copyDatas.append(d[0])
        for s in values:
            for k, v in filterDic.items():
                if v == s:
                    if d[k] not in copyDatas:
                        copyDatas.append(d[k])
                        break
        return copyDatas

if __name__=="__main__":
    us = Report()
    us.mergeCsv()
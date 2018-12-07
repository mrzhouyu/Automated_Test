# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 13:19
# @Author  : YuChou
# @Site    : 
# @File    : test.py
# @Software: PyCharm
import pexpect
import time
import re
import os
import sys
import threading
import queue
import multiprocessing
import signal
class Api():

    def __init__(self,port=22, host="10.230.0.41", user="zhouy", pwd="Zhouy123!"):
        self.port=port
        self.host=host
        self.user=user
        self.pwd=pwd

    def logIn(self):
        #conCli=pexpect.spawn("clish")
        # conCli.expect(">")
        conCli = pexpect.spawn("ssh {}@{}".format(self.user, self.host))
        conCli.expect("password")
        conCli.sendline(self.pwd)
        conCli.expect("$")
        conCli.sendline("pish")
        conCli.expect(">")
        # print(conCli.before.decode())
        return conCli

    def simpleConsole(self, sn):
        con = self.logIn()
        notify_cmd = "notifyFilter sns " + sn
        con.sendline(notify_cmd)
        con.expect("Filter:")
        return con

    def otaGwsl(self,verFile1,verFile2,ver1,ver2,id,sn):
        cmd1 = "putfile url {} id {} type OTAFILE".format(verFile1, id)
        cmd2 = "putfile url {} id {} type OTAFILE".format(verFile2, id)
        con = self.simpleConsole(sn)
        currentVer=self.queryVer(con,id)
        if currentVer=="timeout":
            self.savelog("timeout",id,"before ota")
        else:
            self.twiceJugle(currentVer,id)#判断上一次ota是否判断有误
            if currentVer == ver1:
                self.ota(con, cmd2, ver2, id)

            elif currentVer == ver2:
                self.ota(con, cmd1, ver1, id)
            else:
                self.ota(con, cmd1, ver1, id)

    def queryVer(self, con, id):
        # print("执行到cyclOta")
        con.sendline("queryDeviceInfo id {}".format(id))
        con.expect(["Type Name          GWSL", "timeout"])
        s=re.findall(r"(\d\.\d\.\d{3})", con.before.decode())
        if s != []:
            return s[0]
        else:
            return "timeout"

    def ota(self,con,cmd,ver,id):
        start_time=time.time()
        con.sendline(cmd)
        try:
            con.expect("ok")
        except:
            self.savelog("timeout",id,"before ota ing")
            return None

        time.sleep(180)
        currentVer = self.queryVer(con, id)
        if currentVer == ver:
            end_start = time.time()
            spend_time = re.findall(r'(:\d{2}:\d{2})', time.asctime(time.localtime(end_start - start_time)))[0].strip(':')  # 提取花费的时间
            self.savelog("success",id,ver,spend_time)
        else:
            time.sleep(20)
            currentVer=self.queryVer(con,id)
            if currentVer==ver:
                end_start = time.time()
                spend_time = re.findall(r'(:\d{2}:\d{2})', time.asctime(time.localtime(end_start - start_time)))[0].strip(':')  # 提取花费的时间
                self.savelog("success", id, ver,spend_time)
            else:
                time.sleep(20)
                currentVer=self.queryVer(con,id)
                if currentVer==ver:
                    end_start = time.time()
                    spend_time = re.findall(r'(:\d{2}:\d{2})', time.asctime(time.localtime(end_start - start_time)))[0].strip(':')  # 提取花费的时间
                    self.savelog("success",id,ver,spend_time)
                else:
                    time.sleep(60)
                    currentVer=self.queryVer(con,id)
                    if currentVer==ver:
                        self.savelog("success",id,ver,"time is 280s")
                    else:
                        # print("currentVer:" + currentVer)
                        # print("ver" + ver)
                        self.savelog("failed",id,ver+"F")#先做一次初步判断 加个标志符"Flag" 第二次判断时候再去除


    #为避免第一次ota失败判断是错误的 这里加个重复验证
    def twiceJugle(self,currentver,id):
        filePath="failed" + str(id) + '.txt'
        if os.path.exists(filePath):
            with open(filePath, 'r+') as r:
                datas = r.readlines()
                if datas:
                    data = datas[-1]
                    if "F" in data:
                        failedVer = re.findall(r'(\d\.\d\.\d{3})', data)[0]
                        if failedVer == currentver:  # 当前版本其实是等于失败的版本 初次判断失败了 将其更正为成功 写入成功文件
                            self.savelog("success", id, currentver, "so long time")
                            del datas[-1]
                            with open("failed" + str(id) + '.txt', "w") as w:
                                w.writelines(datas)
                        else:  # 初次判断成功 去掉Flag
                            datas[-1] = datas[-1].replace("F", "")
                            with open("failed" + str(id) + '.txt', "w") as w:
                                w.writelines(datas)
                    else:
                        return None
                else:
                    return None
        else:
            return None




    def savelog(self,status,id,ver,spend_time=''):

        path = status + str(id) + '.txt'
        with open(path, 'a') as f:
            f.write("ota to {} {}. currentTime:{}  spend_time:{}".format(ver,status,time.asctime(time.localtime()),spend_time)+ '\n')

    def main(self):
        idDic={
            # "45" : "5410ec339c23",
            # "46" : "d88039a38743"
            # # "5" : "5410ec33c15a",
            "7" : "5410ec33bb64",
            "10": "d88039a3c10f",
            "12": "5410ec336861",
            "15": "5410ec33d70a",
            "59": "d88039a32f94",
            "14": "5410ec33ba38",
            "21": "d88039a36f49"

        }

        # 并发升级两个版本
        ver1File = "http://10.230.2.36/share/ota/SmartRetail-451-20180929-060816/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.184.ota"
        ver2File = "http://10.230.2.36/share/ota/SmartRetail-453-20181008-041756/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.186.ota"
        ver1="1.0.184"
        ver2="1.0.186"

        #循环次数 0表示无限循环
        cycle=0

        times=0
        while True:
            times+=1
            for i in idDic.keys():
                with open("cal.txt",'a') as f:
                    f.write("Gwsl {} NO.{} time: ".format(i,times)+time.asctime(time.localtime())+'\n')
                # print("Gwsl {} NO.{}".format(i,times))
                self.otaGwsl(ver1File,ver2File,ver1,ver2,i,idDic[i])
            if cycle==0:
                continue
            elif times<cycle:
                continue
            else:
                break


if __name__=="__main__":
    myclass=Api()
    myclass.main()
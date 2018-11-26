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
        time.sleep(10)#等待副网关组网
        currentVer=self.queryVer(con,id)
        if currentVer=="timeout":
            self.savelog("timeout",id,"before ota")
        else:
            # self.twiceJugle(currentVer,id)#判断上一次ota是否判断有误
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
        if currentVer == ver:#3min内升级完
            end_start = time.time()
            spend_time = re.findall(r'(:\d{2}:\d{2})', time.asctime(time.localtime(end_start - start_time)))[0].strip(':')  # 提取花费的时间
            self.savelog("success",id,ver,spend_time)
        else:
            s=1 #等待的20s次数
            while True:#3min内没升级完继续循环等待
                time.sleep(20)
                currentVer=self.queryVer(con,id)
                if currentVer==ver:#3min外升级完
                    end_start = time.time()
                    spend_time = re.findall(r'(:\d{2}:\d{2})', time.asctime(time.localtime(end_start - start_time)))[0].strip(':')
                    self.savelog("success", id, ver, spend_time)
                    break
                else:#s小于10仍然没有升级完
                    end_start = time.time()
                    spend_time = re.findall(r'(:\d{2}:\d{2})', time.asctime(time.localtime(end_start - start_time)))[0].strip(':')
                    if "timeout" in currentVer:#原因是超时 可能是正在重启
                        self.savelog("waitTimeout", id, ver, spend_time)
                    else:#版本仍然没有变 原因可能是 还没重启
                        if s>10:#时间太长默认为升级失败
                            self.savelog("Failed", id, ver, spend_time)
                            break
                s+=1


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
            # "10": "d88039a3c10f",
            "12": "5410ec336861"
            # "15": "5410ec33d70a",
            # "59": "d88039a32f94",
            # "14": "5410ec33ba38",
            # "21": "d88039a36f49"

        }
        # 并发升级两个版本
        ver1File = "http://10.230.2.36/share/ota/470ota/SR-GWSL-M527-A000-FN3-H030-V1.0.199.ota"
        ver2File = "http://10.230.2.36/share/ota/465ota/SR-GWSL-M527-A000-FN3-H030-V1.0.197.ota"
        ver1="1.0.199"
        ver2="1.0.197"

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
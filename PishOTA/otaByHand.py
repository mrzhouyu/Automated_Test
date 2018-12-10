 # -*- coding: utf-8 -*-
# @Time    : 2018/12/5 18:17
# @Author  : YuChou
# @Site    : 
# @File    : otaByHand.py
# @Software: PyCharm

import pexpect
import time
import re
import sys
import threading
import queue
import multiprocessing
from progressbar import *
import os
import shutil

class Api():
    #可配成{"id":"sn",}形式
    GWSL_SLAVE_Json = {}
    GWSL_MASTER_Json = {}
    URL = ""
    URL1 = ""
    def __init__(self, port = 22, host = "10.230.0.41", user = "zhouy", pwd = "Zhouy123!" ):
        print('''1. flag = 0 且times =0-->ota 1次,用来升级主+副用,默认选项;\n2. flag = 1-->ota 1次，升级带wifi的二级网关;\n3.flag = 其他 且 times = 0--> ota forever;\n4. flag = 其他 且 times = somenumber-->循环otasomenumber次.\n*****************************************************************'''.rjust(30))
        self.flag, self.times =self.getOtaModel()
        self.port = port
        self.host = host
        self.user = user
        self.pwd = pwd
        self.otaSuccessList = []
        self.otaFailedList = []
        self.clearWorkspace()
        self.master_List, self.slave_List= self.getOtaId()
        self.url_1, self.url_2 = self.getVersion() #当选择非循环ota模式时候，只有url_1有连接地址
        self.console = self.__logIn()
        self.queue = queue.Queue()
        self.queueOk = queue.Queue()#用于并发循环升级时候记录升级成功的id，用来进行下一次ota

    #工作空间清理
    def clearWorkspace(self):
        if os.path.exists("WorkSpace"):
            yesOrNo = input("存在当前目录，是否能清除工作路径及日志文件(yes/no)")
            if yesOrNo in ["yes","y","Y","YES","Yes"]:
                shutil.rmtree("WorkSpace")
                os.mkdir("WorkSpace")
                os.chdir("WorkSpace")
            else:
                os.chdir("WorkSpace")
        else:
            os.mkdir("WorkSpace")
            os.chdir("WorkSpace")
        print("当前工作目录是 {}".format("WorkSpace"))
    def getOtaModel(self):
        try:    #避输入错误的数据类型
            flag = int(input("输入flag："))
            times = int(input("输入times："))
        except:
            print("输入格式或者数据类型不正确")
            sys.exit(1)
        if not flag or not times:
            return 0,0
        else:
            return flag, times

    #获取交升级设备列表
    def getOtaId(self):
        if not self.GWSL_MASTER_Json or not self.GWSL_SLAVE_Json or not self.URL:
            master_List = input("输入需要ota的主二级网关ID(例如 :1 2 3)：").split(" ")
            slave_List = input("输入需要ota的二级网关副ID(例如 :1 2 3)：").split(" ")
            print("主网关 {}".format(master_List))
            print("副网关 {}".format(slave_List))
            return master_List, slave_List
        else:
            print("主网关 {}".format(list(self.GWSL_MASTER_Json.keys())))
            print("副网关 {}".format(list(self.GWSL_SLAVE_Json.keys())))
            return list(self.GWSL_MASTER_Json.keys()), list(self.GWSL_SLAVE_Json.keys())

    #获取输入模式和版本
    def getVersion(self):
        otaType = input("只升级输入请输入's',循环升级请输入'c' :")
        if otaType == "s":
            url_1 = input("请输入需要升级版本的的url链接：")
            return url_1, ''

        elif otaType == "c":
            url_1 = input("请输入需要升级的版本1的url链接：")
            url_2 = input("请输入需要升级的版本2的url链接：")
            return url_1, url_2
        else:
            print("升级类型选择错误，重新执行程序！")
            sys.exit(1)

    #登陆获取控制台
    def __logIn(self):
        #conCli=pexpect.spawn("clish")
        # conCli.expect(">")
        conCli = pexpect.spawn("ssh {}@{}".format(self.user, self.host))
        conCli.expect("password")
        conCli.sendline(self.pwd)
        conCli.expect("~")
        conCli.sendline("pish 127.0.0.1 6666")
        conCli.expect(">")
        print("login ok")
        conCli.sendline("notifyFilter sns none")
        conCli.expect(">")
        return conCli

    #ota前提条件初始化。。。及开始
    def ota(self, id, url):
        # print("ota函数被调用了......")
        con = self.console
        cmd = "putfile url {} id {} type OTAFILE".format(url, id)
        version = re.findall(r"-V(\d{1,3}\.\d{1,3}\.\d{1,3})\.ota", url)[0]#升级版本
        query = "queryDeviceInfo id {}".format(id)
        con.sendline(query)
        num = con.expect(["Type Name", "timeout", ])
        buff = con.before.decode("utf8")
        if num == 0:
            newVer = re.findall(r"Firmware Version.{1,4}(\d{1,3}\.\d{1,3}\.\d{1,3})", buff)[0]
            if version == newVer:#新旧版本一样直接跳出升级
                status = "failed"
                Time = time.asctime(time.localtime(time.time()))
                logCmd = "GWSL{} BEFORE OTA VERSION IS NEW, END CURRENT OTA, CURRENTTIME: {}".format(id, Time)
                self.saveLog(status, logCmd)
                self.otaFailedList.append(id)
                return
        else:
            status = "failed"
            Time = time.asctime(time.localtime(time.time()))
            logCmd = "GWSL{} BEFORE OTA TIMEOUT, END CURRENT OTA, CURRENTTIME: {}".format(id, Time)
            self.saveLog(status=status, log=logCmd)
            self.otaFailedList.append(id)
            return

        #print("下发ota命令....版本是{}".format(version))
        con.sendline(cmd)
        start_time = time.time()
        num = con.expect(["ok", "timeout"])
        if num == 0:
            status = "ok"
            Time = time.asctime(time.localtime(time.time()))
            logCmd = "GWSL{} OTA PROCESS CALLBACK IS OK, IT IS OTAING, CURRENTTIMR: {}".format(id, Time)
            self.saveLog(status=status, log=logCmd)
            #print("正确的升级返回，正在升级id 是{}的二级网关".format(id))
        else:
            status = "failed"
            Time = time.asctime(time.localtime(time.time()))
            logCmd = "GWSL{} BEFORE OTA TIMEOUT, END CURRENT OTA, CURRENTTIME: {}".format(id, Time)
            self.saveLog(status=status, log=logCmd)
            self.otaFailedList.append(id)
            return
        self.waitLogic(id, con, version, start_time)

    #ota等待及状态判断
    def waitLogic(self, id ,con, version, startTime):
        cmd = "queryDeviceInfo id {}".format(id)
        total = 0 #最多500次查询，目的为了统计ota一次时间
        while True:
            total += 1
            time.sleep(1)
            end_time = time.time()
            con.sendline(cmd)
            num = con.expect(["Type Name", "timeout",pexpect.EOF])
            if num == 0:
                buff = con.before.decode("utf8")
                newVer = re.findall(r"Firmware Version.{1,4}(\d{1,3}\.\d{1,3}\.\d{1,3})", buff)[0]
                if newVer == version:
                    #print("id 为 {} 的二级网关升级成功".format(id))
                    status = "success"
                    spendTime = time.asctime(time.localtime(end_time - startTime))
                    Time = time.asctime(time.localtime(time.time()))
                    logCmd = "GWSL{} OTA TO {} {}, TOTALTIME: {}, CURRENTTIME: {}".format(id, version, status, spendTime, Time)
                    self.otaSuccessList.append(id)
                    self.saveLog(status,logCmd)
                    break
                else:
                    if total >= 500:
                        status = "failed"
                        Time = time.asctime(time.localtime(time.time()))
                        logCmd = "GWSL{} OTA TO {} {},  CURRENTTIME: {}".format(id, version, status, Time)
                        self.saveLog(status, logCmd)
                        self.otaFailedList.append(id)
                        break
                    continue
            else:
                if total >= 500:
                    status = "failed"
                    Time = time.asctime(time.localtime(time.time()))
                    logCmd = "GWSL{} OTA TO {} {}, CURRENTTIME: {}".format(id, version, status, Time)
                    self.saveLog(status, logCmd)
                    self.otaFailedList.append(id)
                    break
                continue
    #日志处理
    def saveLog(self, status, log):

        if status == "success":

            with open("Success.txt", "a", encoding="utf8") as f:
                f.write(log + "\n")
        if status == "failed":
            with open("Failed.txt", "a", encoding="utf8") as f:
                f.write(log + "\n")
        if status == "ok":
            with open("Process.txt", "a", encoding="utf8") as f:
                f.write(log + "\n")
        if status == "total":
            with open("OtaTimes.txt", "a", encoding="utf8") as f:
                f.write(log + "\n")

    def oneMulOta(self, idlist, type = "", otaUrl=''):
        wigets1 = ["Wifi Gwsl Progress:", Percentage(), ' ', Bar("*"), ' ', Timer(), ' ',ETA(), ' ', FileTransferSpeed()]
        wigets2 = ["Master Gwsl Progress:", Percentage(), ' ', Bar("*"), ' ', Timer(), ' ', ETA(), ' ',FileTransferSpeed()]
        wigets3 = ["Slaver Gwsl Progress:", Percentage(), ' ', Bar("*"), ' ', Timer(), ' ', ETA(), ' ',FileTransferSpeed()]

        if type == "master":
            bar = ProgressBar(widgets=wigets2)
        elif type == "slaver":
            bar = ProgressBar(widgets=wigets3)
        else:
            bar = ProgressBar(widgets=wigets1)
        if otaUrl:
            for id in bar(idlist):
                self.ota(id, otaUrl)
        else:
            print("请输入ota链接")
            sys.exit(1)

    #主程序 单线程Ota
    # 1. flag = 0-->ota 1次,用来升级主+副用,默认选项；
    # 2. flag = 1-->ota 1次，升级带wifi的二级网关
    # 2. flag = 其他 且 times = 0--> ota forever，
    # 3. flag = 其他 且 times = somenumber-->循环otasomenumber次

    def main(self):
        if self.flag == 0:
            self.oneMulOta(self.slave_List,type="slaver", otaUrl=self.url_1)
            self.oneMulOta(self.master_List,type="master", otaUrl=self.url_1)
        elif self.flag==1:
            self.oneMulOta(self.master_List,type="other", otaUrl=self.url_1)
        else:
            if self.times == 0:
                status = "total"
                start_time = time.time()
                chooseVersion = 0 #版本交叉的flag变量
                while True:
                    if chooseVersion == 0: #两个版本交叉ota
                        U = self.url_1
                        chooseVersion = 1
                    else:
                        U = self.url_2
                        chooseVersion = 0

                    self.times += 1
                    t = 0.5
                    if len(self.master_List) < 2: #利用主网关的列表长度来判断是否需要你等待所属副网关组网上来
                        t = 20
                    self.oneMulOta(self.slave_List, type="slaver", otaUrl=U)
                    time.sleep(t)  #避免只遇到一个主的情况，主的刚升级完 副的可能还没组网上来
                    self.oneMulOta(self.master_List, type="master", otaUrl=U)
                    spend_time = time.asctime(time.localtime(time.time() - start_time))
                    logCmd = "OTA TIMES TOTAL IS {}, SPENDTIME: {}, CURRENTTIME: {}".format(self.times, spend_time, time.asctime(time.localtime(time.time())))
                    self.saveLog(status, logCmd)
            else:
                status = "total"
                start_time = time.time()
                chooseVersion = 0  # 版本交叉的flag变量
                n = 0
                while 0 < self.times:
                    if chooseVersion == 0: #两个版本交叉ota
                        U = self.url_1
                        chooseVersion = 1
                    else:
                        U = self.url_2
                        chooseVersion = 0
                    self.times += 1
                    self.oneMulOta(self.slave_List, type="slaver", otaUrl=U)
                    self.oneMulOta(self.master_List, type="master", otaUrl=U)
                    spend_time = time.asctime(time.localtime(time.time() - start_time))
                    logCmd = "OTA TIMES TOTAL IS {}, SPENDTIME: {}, CURRENTTIME: {}".format(self.times, spend_time,time.asctime(time.localtime(time.time())))
                    self.saveLog(status, logCmd)

    #在线设备列表
    def onlineDeviceStatus(self):
        con = self.console
        con.sendline("listDevices")
        index = con.expect(["Total"])
        if index == 0:
            CDSCDic = {}
            GWFLDic = {}
            GWSLDic = {}
            lines = con.before.decode().split('\r\n')
            for i, line in enumerate(lines):
                if re.findall(r'(online|offline)', line) != []:
                    if 'CDSC' in line:
                        try:
                            MatchStr = re.sub("\s+",":",line)
                            status = MatchStr[0]
                            id = MatchStr[6]
                            SN = MatchStr[7]
                            version = MatchStr[8]
                            CDSCDic[id] = [status, SN, version]
                        except:
                            continue

                    elif 'GWFL' in line:
                        try:
                            MatchStr = re.sub("\s+",":",line)
                            status = MatchStr[0]
                            id = MatchStr[6]
                            SN = MatchStr[7]
                            version = MatchStr[8]
                            CDSCDic[id] = [status, SN, version]
                        except:
                            continue
                    else:
                        try:
                            MatchStr = re.sub("\s+",":",line)
                            status = MatchStr[0]
                            id = MatchStr[6]
                            SN = MatchStr[7]
                            version = MatchStr[8]
                            CDSCDic[id] = [status, SN, version]
                        except:
                            continue
                else:
                    continue

            return GWFLDic, GWSLDic, CDSCDic
        else:
            print("pish无法连接到一一级网关！")
            sys.exit(1)

    #将设备状态存为json文件到本地
    def dumpDeviceToJson(self):
        DeviceStatus = {}
        GWFLDIC ,GWSLDIC, CDSCDic= self.onlineDeviceStatus()
        #定义字段 一级网关id：GWFLId ， 二级网关id：GWSLId， 称Id：CDSCId；
        #
        DeviceStatus["GWFLDIC"]={}




    #基于onlineDeviceStatus函数的返回，实现自动ota
    def auto_Ota(self):
        pass

    #实例消亡输出
    def __del__(self):
        if self.otaSuccessList:
            print("THIS OTA TEST SUCCESS DEVICE LIST: %s"%self.otaSuccessList)
        if self.otaFailedList:
            print("THIS OTA TEST FAILE DEVICE LIST: %s"%self.otaFailedList)


#多进程 此函数不供if __name__ == "__main__"调用
#只支持单向升级 不支持循环ota
def Multi():
    C = Api()
    master_id = C.master_List
    slaver_id = C.slave_List
    url1 = C.url_1
    # url2 = C.url_2
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    if url1:
        for id in slaver_id:
            pool.apply_async(C.ota, args=(id, url1))
        pool.close()
        pool.join()
        for id in master_id:
            pool.apply_async(C.ota, args=(id,url1))
        pool.close()
        pool.join()


#此处可开启多进程

#Multi()



if __name__ == "__main__":
    C = Api()
    C.main()

    #多线程








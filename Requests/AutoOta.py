# -*- coding: utf-8 -*-
# @Time    : 2018/9/28 15:28
# @Author  : YuChou
# @Site    : 
# @File    : AutoOta.py
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
import json
class Filter():

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
        # print("登陆成功")
        # print(conCli.before.decode())
        return conCli
    #找到一级网下所有设备id 版本 状态
    def queryDeviceStatus(self,sn='b827eb53e5aa'):
        con = self.logIn()
        notify_cmd = "notifyFilter sns " + sn
        con.sendline(notify_cmd)
        con.expect("Filter")
        con.sendline("listDevices")
        con.expect("Total:")
        lines=con.before.decode().split('\r\n')
        CDSCDic={}
        GWFLDic={}
        GWSLDic={}
        for i,line in enumerate(lines):
            if re.findall(r'(online|offline)',line)!=[]:
                if 'CDSC' in line:
                    try:
                        MatchStr=re.findall(r'(online|offline).+CDSC-(\d{1,3}).+ ([a-zA-Z0-9]{11,12}) .+(\d{1,3}\.\d{1,3}\.\d{1,3})',line)
                        id = MatchStr[0][1].lstrip('0')
                        status = MatchStr[0][0]
                        SN = MatchStr[0][2]
                        version = MatchStr[0][3]
                        CDSCDic[id] = [status, SN, version]
                    except:
                        continue

                elif 'GWFL' in line:
                    try:
                        MatchStr=re.findall(r'(online|offline).+GWFL-(\d{1,3}).+ ([a-zA-Z0-9]{11,12}).+(\d{1,3}\.\d{1,3}\.\d{1,3})',line)
                        id = MatchStr[0][1].lstrip('0')
                        status = MatchStr[0][0]
                        SN = MatchStr[0][2]
                        version = MatchStr[0][3]
                        GWFLDic[id] = [status, SN, version]
                    except:
                        continue

                else:
                    try:
                        MatchStr=re.findall(r'(online|offline).+GWSL-(\d{1,3}).+ ([a-zA-Z0-9]{11,12}) .+(\d{1,3}\.\d{1,3}\.\d{1,3})',line)
                        id = MatchStr[0][1].lstrip('0')
                        status = MatchStr[0][0]
                        SN = MatchStr[0][2]
                        version = MatchStr[0][3]
                        GWSLDic[id] = [status, SN, version]
                    except:
                        continue
            else:
                continue
        print(GWSLDic)
        return GWFLDic,GWSLDic,CDSCDic

    def saveJson(self):

        pass

    def onlineGwsl(self):
        GWSLDic=self.queryDeviceStatus()[1]
        onlineGwslList=[]
        for i in GWSLDic.keys():
            if GWSLDic[i][0]=="online":
                onlineGwslList.append(i)
        # print(onlineGwslList)
        return onlineGwslList,GWSLDic


    def offlineGwsl(self):
        GWSLDic=self.queryDeviceStatus()[1]
        offlineGwslList=[]
        for i in GWSLDic.keys():
            if GWSLDic[i][0]=="offline":
                offlineGwslList.append(i)
        return offlineGwslList,GWSLDic





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
        # print("登陆成功")
        # print(conCli.before.decode())
        return conCli

    def simpleConsole(self, sn):
        print("sn 是{}".format(sn))
        con = self.logIn()
        notify_cmd = "notifyFilter sns " + sn
        con.sendline(notify_cmd)
        con.expect("Filter")
        return con

    def otaGwsl(self,url,version,id,sn):
        cmd = "putfile url {} id {} type OTAFILE".format(url, id)
        con = self.simpleConsole(sn)
        currentVer=self.queryVer(con,id)
        self.ota(con, cmd, version, id)

    #info指定设备 查看设备版本状态
    def queryVer(self, con, id):
        # print("执行到cyclOta")
        con.sendline("queryDeviceInfo id {}".format(id))
        con.expect(["Type Name          GWSL", "timeout"])
        s=re.findall(r"(\d\.\d\.\d{3})", con.before.decode())
        if s != []:
            return s[0]
        else:
            time.sleep(20)
            con.sendline("queryDeviceInfo id {}".format(id))
            con.expect(["Type Name          GWSL", "timeout"])
            # ver = re.findall(r"(\d\.\d\.\d{3})", con.before.decode())[0]
            s=re.findall(r"(\d\.\d\.\d{3})", con.before.decode())
            if s !=[]:
                return s[0]
            else:
                return "timeout"


    def ota(self,con,cmd,ver,id):
        print("正在升级id是{}的二级网关".format(id))
        start_time=time.time()
        con.sendline(cmd)
        try:
            con.expect("ok")
        except:
            print("无法正确升级")
            return None

        time.sleep(150)
        currentVer = self.queryVer(con, id)
        if currentVer == ver:
            print("ota successful")

        else:
            time.sleep(20)
            currentVer=self.queryVer(con,id)
            if currentVer==ver:
                print("ota successful")
            else:
                time.sleep(20)
                currentVer = self.queryVer(con, id)
                if currentVer==ver:
                    print("ota successful")
                else:
                    print("ota failed")
                    return None


    def savelog(self,status,id,ver,spend_time=''):

        path = status + str(id) + '.txt'
        with open(path, 'a') as f:
            f.write("ota to {} {}. currentTime:{}  spend_time:{}".format(ver,status,time.asctime(time.localtime()),spend_time)+ '\n')

    #执行ota
    def execute(self,otadic,FileUrl,ver1):
        idDic=otadic
        #单进程
        for i in idDic.keys():
            print("{}   {}   {}   {}".format(FileUrl,ver1,i,idDic[i]))
            self.otaGwsl(FileUrl,ver1,i,idDic[i])
        #多进程
        # otaPool=multiprocessing.Pool(3)




if __name__=="__main__":

    executeClass=Api()

    #客户需求
    otaUrl=input("请输入Http升级包连接地址(例如：http://10.230.2.36/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.176.ota)：")
    otaVer=input("请输入需要ota的GWSL版本(例如：1.0.176)：")

    #查看当前当前所在环境设备情况的实例
    FilterClass=Filter()
    onlineId,GWSLdic=FilterClass.onlineGwsl()
    print("在线GWSL设备列表：%s"%onlineId)
    needOta={}
    for i in onlineId:
        if GWSLdic[i][2]!=otaVer:
            needOta[i]=GWSLdic[i][2]
    print("如下为可升级的二级网关id：==>{}     其对应的旧版本对应：{}".format(list(needOta.keys()),needOta))
    needId=input("请输入你需要升级的ID(例如:1,2,3) 若全部升级请输入0:").split(',')
    #ota参数参数传入选择语句
    otaDic = {}
    if needId[0]=='0':
        for j in needOta.keys():
            otaDic[j]=GWSLdic[j][1]
        executeClass.execute(otaDic,otaUrl,otaVer)#调用执行函数
        print("Task is Ok!")
    else:
        for j in needId:
            otaDic[j]=GWSLdic[j][1]
        executeClass.execute(otaDic,otaUrl,otaVer)#调用执行函数
        print("Task is Ok!")






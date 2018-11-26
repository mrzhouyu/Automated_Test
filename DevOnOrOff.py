# -*- coding: utf-8 -*-
# @Time    : 2018/9/28 15:28
# @Author  : YuChou
# @Site    :
# @File    : AutoOta.py
# @Software: PyCharm
import pexpect
import time
import re
# import os
# import sys
# import threading
# import queue
# import multiprocessing
# import signal
# import json
class Filter():

    def __init__(self,port=22, host="10.230.0.41", user="zhouy", pwd="Zhouy123!"):
        self.port=port
        self.host=host
        self.user=user
        self.pwd=pwd
        self.con=self.logIn()#登陆
        self.queryTotalId()#info 不在线设备 防止假状态
        self.datas=self.queryDeviceStatus()#返回此时设备在线状态

    def logIn(self):
        #conCli=pexpect.spawn("clish")
        # conCli.expect(">")
        conCli = pexpect.spawn("ssh {}@{}".format(self.user, self.host))
        conCli.expect("password")
        conCli.sendline(self.pwd)
        conCli.expect("$")
        conCli.sendline("pish 127.0.0.1 7777")
        conCli.expect(">")
        # print("登陆成功")
        # print(conCli.before.decode())
        return conCli

    #找到一级网下所有设备id 版本 状态
    def showList(self,sn ='b827ebb59c45'):
        con = self.con
        notify_cmd = "notifyFilter sns " + sn
        con.sendline(notify_cmd)
        con.expect("Filter")
        con.sendline("listDevices")
        con.expect("Total:")
        lines=con.before.decode().split('\r\n')
        return lines

    def queryTotalId(self):
        con=self.con
        lines=self.showList()
        for i,line in enumerate(lines):
            if re.findall(r'(offline)',line)!=[]:
                MatchStr = re.findall(r'(offline).+(GWSL|CDSC)-(\d{1,3}).+ ([a-zA-Z0-9]{11,12}) .+(\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                device=MatchStr[0][1]
                id = MatchStr[0][2].lstrip('0')
                cmd="queryDeviceInfo id "+id
                con.sendline(cmd)
                x=con.expect(["GWSL","timeout","CDSC","GWFL",pexpect.TIMEOUT,pexpect.EOF])
                time.sleep(0.3)
                # print("{} queryId {}".format(device, id))

    def queryDeviceStatus(self,sn='none'):
        lines=self.showList()
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
  #      print(GWSLDic)
        return GWFLDic,GWSLDic,CDSCDic

    def saveJson(self):

        pass

    def onlineGwsl(self):
        GWSLDic=self.datas[1]
        onlineGwslList=[]
        for i in GWSLDic.keys():
            if GWSLDic[i][0]=="online":
                onlineGwslList.append(i)
        # print(onlineGwslList)
        return onlineGwslList,GWSLDic


    def offlineGwsl(self):
        GWSLDic=self.datas[1]
        offlineGwslList=[]
        for i in GWSLDic.keys():
            if GWSLDic[i][0]=="offline":
                offlineGwslList.append(i)
        return offlineGwslList,GWSLDic


if __name__=="__main__":
    ins=Filter()
    message1=ins.onlineGwsl()
    message2=ins.offlineGwsl()
    print("current time: {}".format(time.asctime(time.localtime(time.time()))))
    print("Total {} online: {}".format(len(message1[0]),message1[0]))
    print("Total {} offline: {}".format(len(message2[0]),message2[0]))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print("onlineDetail: {}".format(message1[1]))
    #print("offlineDetail: {}".format(message2[1]))



# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 10:19
# @Author  : YuChou
# @Site    : 
# @File    : OTATest.py
# @Software: PyCharm
from pexpect.pxssh import pxssh
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


    def __init__(self,port=22,host="10.230.2.226",user="pi",pwd="root"):
        self.port=port
        self.host=host
        self.user=user
        self.pwd=pwd

    def logIn(self):
        #conCli=pexpect.spawn("clish")
        # conCli.expect(">")
        conCli=pexpect.spawn("ssh {}@{}".format(self.user,self.host))
        conCli.expect("password:")
        conCli.sendline(self.pwd)
        conCli.expect("[#$]")
        conCli.sendline("clish")
        conCli.expect(">")
        return conCli

    def executeLongOta(self,ver1,ver2,id,times,n=1):
        cmd1 ="putfile {} {} ota".format(id,ver1)
        cmd2 = "putfile {} {} ota".format(id,ver2)
        conCli=self.logIn()
        cmd1_ver=re.findall("(\d\.\d\.\d{3})",cmd1)[0]
        cmd2_ver=re.findall("(\d\.\d\.\d{3})",cmd2)[0]
        conCli.sendline("info %s" % id)
        conCli.expect([">"],timeout=10)
        returnDates=conCli.before.decode()
        while "out" in returnDates:
            time.sleep(5)
            conCli.sendline("info %s" % id)
            conCli.expect([">"], timeout=10)
            self.log_Log(id,"timeout","timeout",n)
            returnDates = conCli.before.decode()

        reg_Oldver=re.findall("Firmware Version: (\d\.\d\.\d{3})",returnDates)[0]
        print("GWSL-id%s current version is %s" % (id, reg_Oldver))
        if reg_Oldver==cmd1_ver:

            conCli.sendline(cmd2)
            print("发送完cmd2命令 :cmd1>>>cmd2")
            self.jugle(conCli,cmd2_ver,id,n)
            self.cyc(ver1, ver2, id, times,n=n+1)

        elif reg_Oldver==cmd2_ver:
            conCli.sendline(cmd1)
            print("发送完cmd1命令 :cmd2>>>cmd1")
            self.jugle(conCli, cmd1_ver,id,n)
            self.cyc(ver1, ver2, id, times,n=n+1)

        else:
            conCli.sendline(cmd1)
            print("发送完cmd1命令  cmd>>>cm1")
            self.jugle(conCli, cmd1_ver,id,n)
            self.cyc(ver1,ver2,id,times,n=n+1)


    def cyc(self,ver1,ver2,id,times,n):
        if times==0:
            self.executeLongOta(ver1,ver2,id,times,n)
        elif times-1<1:
            print("over current ota")
            pid=os.getppid()
            #os.kill(pid,signal.SIGKILL)#linux下
            print("pid is %s"%pid)
            os.popen('taskkill.exe /pid:'+str(pid))
        else:
            self.executeLongOta(ver1,ver2,id,times=times-1,n=n)


    def jugle(self,conCli,ver,id,n):
        print("Waiting for ota")
        time.sleep(120)
        conCli.expect('>')
        buff=self.try_info(conCli,id)
        if "out" in buff:
            self.log_Log(id,"timeout",'timeout',n)
        print("Jugle Success or Faild!")
        exp1= "Firmware Version: %s"%ver
        exp2="100%  Upload OTA GWSL-0{}(ID:{})".format(id,id)
        if exp1 in buff or exp2 in buff:
            if exp1 in buff:
                self.log_Log(id, "success", ver, n)
                print("it is Ok")
            else:
                self.log_Log(id, "faild", ver, n)
                print("it is Faild")
        else:
            # print('first time is faild')
            i=1
            while True:
                time.sleep(17)
                conCli.sendline('info %s' % id)
                conCli.expect(">")
                conCli.sendline('info %s' % id)#避免其他网关log干扰
                conCli.expect(">")
                buff=conCli.before.decode()
                if exp1 in buff or exp2 in buff:
                    if exp1 in buff:
                        self.log_Log(id, "success",ver,n)
                        print("it is Ok")
                    else:
                        self.log_Log(id, "faild", ver, n)
                        print("it is Faild")
                    break
                i=i+1
                if i>3:
                    self.log_Log(id,"faild",ver,n)
                    print("it is Faild")
                    break

    def log_Log(self,id,status,ver,n):
        if status:
            print("saving log!")
            if status=="success" or status=="faild":
                with open(status+str(id)+'.txt','a') as f:
                    f.write("GWSL-id{} ota {} {} time: ".format(id,ver,status)+time.asctime(time.localtime())+' number %s'%str(n)+'\n')
            if status=="timeout":
                with open(status+str(id)+'.txt','a') as f:
                    f.write("GWSL-id :{} find {}  time: ".format(id,status)+time.asctime(time.localtime())+' number %s'%str(n)+'\n')


    def try_info(self,conCli,id,times=3):
        conCli.sendline('info %s'%id)
        conCli.expect(">")
        conCli.sendline('info %s' % id)#info两次避免其他ota日志干扰
        conCli.expect(">")
        buff=conCli.before.decode()
        if "out" in buff and times>0:
            buff=self.try_info(conCli,id,times=times-1)
        return buff

    def try_change(self):
        pass

if __name__=="__main__":
    #times=0 无限循环ota 其他表示循环ota次数
    times=5
    OtaClass=Api()
    #并发升级两个版本
    ver1="http://10.230.2.36/share/ota/SmartRetail-372-20180906-173826/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.151.ota"
    ver2="http://10.230.2.36/share/ota/SmartRetail-387-20180910-114726/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.159.ota"
    idList=[45]#并发设备列表
    ThreadPool=multiprocessing.Pool(4)
    for id in idList:
        print("进行中...")
        #time.sleep(5)#尽量避免两个同时升级
        ThreadPool.apply_async(func=OtaClass.executeLongOta,args=(ver1,ver2,id,times))
    ThreadPool.close()#不再加入新的进程
    ThreadPool.join()

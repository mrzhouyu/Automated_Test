# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 9:15
# @Author  : YuChou
# @Site    : 
# @File    : ConPishOta.py
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
        self.port = port
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
        print("登陆成功")
        # print(conCli.before.decode())
        return conCli

    def simpleConsole(self, id, sn):
        con = self.logIn()
        notify_cmd = "notifyFilter sns " + sn
        con.sendline(notify_cmd)
        con.expect('Filter:')
        # print(con.before.decode())
        # print("已经过滤")
        con.sendline("queryDeviceInfo id {}".format(id))
        con.expect(["Type Name          GWSL","timeout"])
        # print(con.before.decode())
        if "Status             online" not in con.before.decode():
            self.saveAnyLog(id, "timeout" ,'GWSL status timeout')
            n=0
            while True:
                n=n+1
                time.sleep(1)
                con.sendline("queryDeviceInfo id {}".format(id))
                con.expect(["Type Name          GWSL","timeout"])
                if "Status             online" not in con.before.decode() and n <6:
                    self.saveAnyLog(id, "timeout", 'GWSL status timeout ')
                    # print(con.before.decode())
                    continue
                elif "Status             online" in con.before.decode():
                    break
                else:
                    self.saveAnyLog(id, "timeout", 'GWSL status timeout last try times')
                    pid = os.getppid()
                    # os.kill(pid,signal.SIGKILL)#linux下
                    print("pid is %s" % pid)
                    os.popen('taskkill.exe /pid:' + str(pid))
                    return None

            # notify_cmd = "notifyFilter sns " + sn
            # con.sendline(notify_cmd)
            # con.expect(">")

            return con

        else:
            # notify_cmd = "notifyFilter sns " + sn
            # con.sendline(notify_cmd)
            # con.expect("Filter:")
            return con


    def gwslOta(self, id ,sn ,ver1File, ver2File, ver1 ,ver2,times):
        # print("执行到gwslOta")
        cmd1="putfile url {} id {} type OTAFILE".format(ver1File,id)
        cmd2="putfile url {} id {} type OTAFILE".format(ver2File,id)
        con=self.simpleConsole(id, sn)
        number = 0
        if times==0:
            while True:
                number = number + 1
                return_status=self.cyclOta(con, id, cmd1, cmd2, ver1, ver2,number)
                if return_status=="ok":
                    continue
                else:
                    print("二级网关超时")
        else:
            while times>0:
                times = times - 1
                number = number + 1
                print("id{} 第{} 次循环".format(id, number) )
                return_status=self.cyclOta(con, id, cmd1, cmd2, ver1, ver2,number)
                if return_status == "ok":
                    continue
                else:
                    print("二级网关超时")



    #ota部分
    def cyclOta(self,con,id,cmd1,cmd2,ver1,ver2,number):
        # print("执行到cyclOta")
        currentVer = self.queryVer(con, id)
        if currentVer=="error":
            return ""
        else:
            if currentVer == ver1:
                print("GWSL {} ota {} to {}".format(id, currentVer, ver2))
                self.ota(con, cmd2, id, ver2,number)
            elif currentVer == ver2:
                print("GWSL {} ota {} to {}".format(id, currentVer, ver1))
                self.ota(con, cmd1, id, ver1,number)
            else:
                print("GWSL {} ota {} to {}".format(id, currentVer, ver1))
                self.ota(con, cmd1, id, ver1, number)
            return "ok"


    def queryVer(self,con,id):
        # print("执行到cyclOta")
        con.sendline("queryDeviceInfo id {}".format(id))
        con.expect(["Type Name          GWSL","timeout"])
        ver=re.findall(r"(\d\.\d\.\d{3})",con.before.decode())[0]
        if ver!="":
            return ver
        else:
            time.sleep(20)
            con.sendline("queryDeviceInfo id {}".format(id))
            con.expect(["Type Name          GWSL", "timeout"])
            ver = re.findall(r"(\d\.\d\.\d{3})", con.before.decode())[0]
            if ver!="":
                return ver
            else:
                return "error"


    def saveAnyLog(self, id, status, strs):
        # print("存日志{}  {} {}".format(id,status,strs))
        path=status+id+".txt"
        with open(path, 'a') as f:
            f.write(strs+time.asctime(time.localtime())+'\n')


    def ota(self,con,cmd,id,ver,number):
        # print("执行到Ota")
        con.sendline(cmd)
        con.expect("ok")
        time.sleep(180)
        currentVer=self.queryVer(con,id)
        if currentVer == ver:
            self.saveAnyLog(id, "success", "times: {}  GWSL {} ota try {} times to {} success ".format(number,id, "1", ver))
        else:
            i=0
            while True:
                i+=1
                time.sleep(10)
                if i>4:
                    self.saveAnyLog(id, "Failed", "times: {} GWSL {} ota try {} times to {} Failed ".format(number,id, i-1, ver))
                    break
                else:
                    currentVer = self.queryVer(con,id)
                    if currentVer == ver:
                        self.saveAnyLog(id, "success", "times :{} GWSL {} ota try {} times to {} success ".format(number,id, i, ver))
                        break
                    else:
                        self.saveAnyLog(id, "Failed", "times :{}GWSL {} ota try {} times to {} Failed ".format(number,id, i, ver))

    def main(self):
        #times 为循环字段 当为0时 表示无限循环ota  times=n时，表示循环otan次
        times = 1500


        idDic={
            # "45" : "5410ec339c23",
            # "46" : "d88039a38743"
            # "5" : "5410ec33c15a",
            "7" : "5410ec33bb64",
            "10": "d88039a3c10f",
            "12": "5410ec336861",
            "15": "5410ec33d70a",
            "17": "5410ec337f61",
            "19": "5410ec33bb6c",
            "21": "d88039a36f49"

        }


        # 并发升级两个版本
        ver1File = "http://10.230.2.36/share/ota/SmartRetail-372-20180906-173826/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.151.ota"
        ver2File = "http://10.230.2.36/share/ota/SmartRetail-387-20180910-114726/ota/SR-GWSL-M527-A000-FN3-H030-V1.0.159.ota"
        ver1="1.0.151"
        ver2="1.0.159"
        ThreadPool = multiprocessing.Pool(8)
        for id in idDic.keys():
            print("进行中...")
            # time.sleep(5)#尽量避免两个同时升级
            ThreadPool.apply_async(func=self.gwslOta, args=(id, idDic[id], ver1File, ver2File, ver1, ver2, times))
        ThreadPool.close()  # 不再加入新的进程
        ThreadPool.join()


if __name__ == "__main__":
    myClass = Api()
    myClass.main()
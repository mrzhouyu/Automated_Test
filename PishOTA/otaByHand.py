 # -*- coding: utf-8 -*-
# @Time    : 2018/12/5 18:17
# @Author  : YuChou
# @Site    : 
# @File    : otaByHand.py
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

    def __init__(self, port = 22, host = "10.230.0.41", user = "zhouy", pwd = "Zhouy123!" ):
        self.port = port
        self.host = host
        self.user = user
        self.pwd = pwd
        self.idList, self.url = self.getOtaId()
        self.console = self.__logIn()
        self.queue = queue.Queue()

    def getOtaId(self):
        idList = input("输入需要ota的二级网关ID：(例如 :1 2 3)").split(" ")
        url = input("请输入升级包url链接：")
        print("idlist is {}".format(idList))
        print("url is {}".format(url))
        return idList, url

    def __logIn(self):
        #conCli=pexpect.spawn("clish")
        # conCli.expect(">")
        conCli = pexpect.spawn("ssh {}@{}".format(self.user, self.host))
        conCli.expect("password")
        conCli.sendline(self.pwd)
        conCli.expect("~")
        conCli.sendline("pish 127.0.0.1 6666")
        conCli.expect(">")
        print("登陆成功")
        conCli.sendline("notifyFilter sns none")
        conCli.expect(">")
        return conCli

    def ota(self, id, url):
        cmd = "putfile url {} id {} type OTAFILE".format(url, id)
        con = self.console
        con.sendline(cmd)
        print("ota ing")
        num = con.expect(["ok", "timeout"])
        if num == 0:
            print("正在升级id 是 {}的二级网关".format(id))
        else:
            print("该二级网关超时。。。")
            self.queue.put(id)
            return None

        version = re.findall(r"-V(\d{1,3}\.\d{1,3}\.\d{1,3})\.ota", url)[0]
        self.waitLogic(id, con, version)

    def waitLogic(self, id ,con, version):
        time.sleep(240)
        cmd = "queryDeviceInfo id {}".format(id)
        con.sendline(cmd)
        num = con.expect(["Type Name", "timeout",])
        if num == 0:
            buff = con.before.decode("utf8")
            newVer = re.findall(r"Firmware Version.{1,4}(\d{1,3}\.\d{1,3}\.\d{1,3})", buff)[0]
            if newVer == version:
                print("id 为 {} 的二级网关升级成功".format(id))
                return
            else:
                self.queue.put(id) #升级失败的放到队列后续升级
        else:
            self.queue.put(id)

    def repeatOta(self, id, url):
        self.ota(id ,url)

    def result(self):
        pass

    def main(self):
        print("升级中...")
        pool = multiprocessing.Pool(4)
        for id in self.idList:
            pool.apply_async(self.ota, args=(id, self.url))
        pool.close()
        pool.join()
        r = 0

        while not self.queue.empty():
            Rpool = multiprocessing.Pool(4)
            if not self.queue.empty():
                Rpool.apply_async(self.repeatOta, args=(self.queue.get(), self.url))
            Rpool.close()
            Rpool.join()
            r += 1
            if r > 3:
                L = []
                while not self.queue:
                    L.append(self.queue.get())
                print("没有升级完成的二级网关id列表： {}".format(L))
            break


if __name__ == "__main__":
    C = Api()
    C.main()

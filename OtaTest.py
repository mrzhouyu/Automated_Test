# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 17:13
# @Author  : YuChou
# @Site    : 
# @File    : OtaTest.py
# @Software: PyCharm


import multiprocessing
import pexpect
import threading

class OTAClass():
    def __init__(self):
        pass

    def test(self):
        console=pexpect.spawn("clish")
        console.expect(">")
        console.sendline("info 14")
        console.expect(">")
        print(console.before.decode())

    def thread(self,Idlist):
        threadPool=[]
        for i in Idlist:
            thread=threading.Thread(target=self.ota(),args=(i,))
            threadPool.append(thread)
        for t in threadPool:
            t.setDaemon(True)
            t.start()
        t.join()
        print("执行完毕！")

    def mulit(self):
        q=multiprocessing.Queue()



    def ota(self):
        pass




if __name__=="__main__":
    pass
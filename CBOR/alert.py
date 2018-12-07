# -*- coding: utf-8 -*-
# @Time    : 2018/12/3 17:18
# @Author  : YuChou
# @Site    : 
# @File    : alert.py.py
# @Software: PyCharm
import pexpect
# import paramiko
import time
HOST = "10.230.1.11"
PORT = 22
PWD = "megvii"
USER = "face"
ROWS = "400"
FILEALL = "10000"

class API():
    def __init__(self, host=HOST, user=USER, pwd=PWD, port=PORT):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.console = self.conPish()

    def conPish(self):
        print("连接RK....")
        console = pexpect.spawn("ssh {}@{} -p {}".format(self.user,self.host, self.port))
        #第一次可能链接不上 开启此语句
        # if console.expect("yes/no",timeout=5):
        #     console.sendline("yes")
        console.expect("[Pp]assword:")
        console.sendline(self.pwd)
        print("登陆完成....")
        console.expect(":~")#pexpect包不能用$作为expect
        return console

    def executeSh(self):
        try:
            self.console.sendline("sudo -s")
            self.console.expect("#")
            self.console.sendline("cd /home/face/zyWorkspace")
            self.console.expect("#")
            self.console.sendline("rm -rf *.log")
            self.console.expect("#")
            self.console.sendline("nohup ./alert.sh {} {} &".format(ROWS, FILEALL))
            self.console.expect("#")
            print("执行完统计脚本,等待程序结束完成....")
            while True:
                self.console.sendline("ls")
                index = self.console.expect(["result","#"])
                if index == 0:
                    time.sleep(1)
                    self.console.sendline("cat result.log")
                    self.console.expect("#")
                    self.console.sendline("cat result.log")
                    self.console.expect("#")
                    print("本次结果：")

                    buff = self.console.before.ecode("utf8").split("\r\n")
                    for n, b in enumerate(buff[1:5]):
                        print("row {}---data {}".format(n, b))
                    self.console.sendline("exit")
                    break
            print("测试结束....")
        except :
            print("远程脚本执行出错,请登陆手动执行~ ip:10.230.1.11")
            return


    def createIamcome(self):
        self.console.sendline("touch iamcome")
        self.console.expect(":~")
        self.console.sendline("exit")
        print("退出")
        return self


if __name__ == "__main__":
    api = API()
    api.createIamcome()
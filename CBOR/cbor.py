# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 13:37
# @Author  : YuChou
# @Site    : 
# @File    : cbor.py
# @Software: PyCharm
import serial
import csv
import time
import conf as conf
import sys
import signal
import time
import alert as alert
import multiprocessing
import re

alert.HOST = "10.230.1.11"
alert.PORT = 22
alert.PWD = "megvii"
alert.USER = "face"
alert.ROWS = "1200"
alert.FILEALL = "5000"

'''
这里是模式配置命令,已经二进制化
'''

model_list = [conf.MODE_ACK, conf.MODE1_SEND, conf.MODE2_SEND, conf.MODE3_SEND, conf.MODE4_SEND, conf.MODE5_SEND,
              conf.MODE6_SEND,
              conf.MODE7_SEND, conf.MODE8_SEND, conf.MODE9_SEND, conf.MODE10_SEND, conf.MODE11_SEND]


class X_Cbor():

    def __init__(self):
        self.warningFun()
        self.com1, self.com2 = self.putCom()
        self.model = self.modelChose()
        # self.ser = self.openCom()
        # self.CsvDatas = self.readCsv()


    def exeDisScript(self):
        api = alert.API()
        api.executeSh()

    def warningFun(self):
        print("请确保二级网关于485断开.....")
        print("确保RK的watchdog.sh已经关闭，gw3399进入测试模式,3s后进入测试....")
        time.sleep(3)

    #获取串口
    def putCom(self):
        com1 = input("请输入当前使用的打印串口编号(例如：1):")
        com2 = input("请输入当前使用的485串口编号（例如：1）")
        # com1 = "com" + com1
        # com2 = "com" + com2
        com1 = "/dev/ttyS" + com1
        com2 = "/dev/ttyS" + com2
        # print("当前使用串口为：%s"%com)
        return com1, com2

    #获取模式
    def modelChose(self):
        mode1 = input("请输入测试模式代号（范围：1~11, ACK模式输入：a）：")
        print("当前选择模式%s"%mode1)
        if mode1 == 'a':
            TestModel = model_list[0]
            return TestModel
        elif mode1 in list(map(lambda x:str(x),list(range(1,12)))):
            TestModel = model_list[int(mode1)]
            return TestModel
        else:
            print("测试代号输入错误，重新执行本程序")
            sys.exit(1)

    #打开串口返回串口对象
    def openCom(self,com):
        print("串口初始化.......")
        ser = serial.Serial(com, 115200, timeout=0.5)
        try:
            if ser.is_open:
                print("串口已打开")
                return ser
            else:
                print("串口已打开")
                ser.open()
                return ser
        except:
            print("串口打开错误，请检查串口是否正确或者是否被占用")
            sys.exit(1)


    #读取串口数据
    def readCom(self,com):
        ser = self.openCom(com)
        while True:
            Flag = str(ser.readline())
            print(Flag)
            if re.search(r"report event cnt", Flag):
                print("开始发送事件，执行远程shell统计脚本")
                break
        ser.close()


    #写入测试模式
    def writeCom(self):
        print("打开写入串口：")
        ser = self.openCom(self.com2)
        print("发送%s"%self.model)
        ser.write(self.model)
        n = 1
        while True:
            print(str(ser.readline()))
            if n == 20:
                break
            n = n+1
        ser.close()
        print("模式已经输入，请连接二级网关485接口")
        time.sleep(2)
        ser.close()

    #预留函数备用
    def readCsv(self):
        D_list = []
        with open("log.csv", "r", encoding="utf8") as f:
            lines = csv.reader(f)
            for line in lines:
                D_list.append(line)
        return D_list

    def main(self):
        self.writeCom() #开启模式
        self.readCom(self.com1) #上报打印信息
        self.exeDisScript() #执行远程脚本

    def __del__(self):
        print("感谢使用")

if __name__ == "__main__":
    query = X_Cbor()
    query.main()

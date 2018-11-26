# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 13:37
# @Author  : YuChou
# @Site    : 
# @File    : cbor.py
# @Software: PyCharm
import flynn
import serial
import cbor2

COM = "com7"
CSVPATH = ""
transfer = {

}

class X_Cbor():
    def __init__(self):
        self.ser = self.openCom()

    def openCom(self):
        ser = serial.Serial(COM, 115200, timeout=0.5)
        if ser.is_open:
            return ser
        else:
            ser.open()
            return ser

    def readCom(self):
        pass

    def writeCom(self):
        pass

    def readCsv(self):
        pass

    def createReport(self):
        pass

    def sendReport(self):
        pass

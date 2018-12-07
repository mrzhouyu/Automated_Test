# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 12:27
# @Author  : YuChou
# @Site    : 
# @File    : testCOM.py
# @Software: PyCharm
import serial
import time
MODE1_SEND = "\x5A\xFF\xFF\x08\xA4\x7E\x3C\xB0\xA3\x63\x63\x6D\x64\x5A\xFF\xFF\x08\x29\x69\x73\x63\x65\x6E\x65\x43\x6F\x5A\xFF\xFF\x08\x4A\x6E\x66\x63\x6D\x69\x64\x64\x75\x5A\xFF\xFF\x08\x54\x75\x69\x64\x69\x73\x63\x65\x6E\x5A\xFF\xFF\x08\x3F\x65\x4D\x6F\x64\x65\x00\xD7\x7E"


def openCom():
    ser = serial.Serial("com7", 115200, timeout=0.5)
    if ser.is_open:
        return ser
    else:
        ser.open()
        return ser
com =openCom()
while True:
    com.write(MODE1_SEND.encode())
    time.sleep(2)
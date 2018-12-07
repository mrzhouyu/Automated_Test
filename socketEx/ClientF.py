# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 16:20
# @Author  : YuChou
# @Site    : 
# @File    : ClientF.py
# @Software: PyCharm
import socket
import socket
HOST = "10.230.0.96"
PORT = 10000

s  = socket.socket()
s.connect((HOST, PORT))


# cmd = "it is cbor file"
# s.send(cmd)
data = s.recv(2048)
print("it is str from server %s"%data)
s.close()
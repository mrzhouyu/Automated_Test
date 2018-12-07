# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 16:20
# @Author  : YuChou
# @Site    : 
# @File    : ServerF.py
# @Software: PyCharm
import socket
HOST = "10.230.1.121"
PORT = 10000

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Client Addr %s'%addr)
    while True:
        data = conn.recv(2048)
        print("Recv data is %s"%data)
        conn.send(bytes("it is cbor"))

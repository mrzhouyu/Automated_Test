# -*- coding: utf-8 -*-
# @Time    : 2018/12/8 16:39
# @Author  : YuChou
# @Site    : 
# @File    : testone.py
# @Software: PyCharm

import multiprocessing
import time
import threading


class Demo:
    def __init__(self, thread_num=5):
        self.thread_num = thread_num

    def productor(self, i):
        print("thread-%d start" % i)

    def start(self,num):
        global y
        y =100
        threads = []
        for x in range(num):
            t = threading.Thread(target=self.productor, args=(x,))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print('all thread end')
    d


if __name__ == "__mian__":
    demo = Demo()
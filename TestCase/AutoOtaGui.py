# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 18:26
# @Author  : YuChou
# @Site    : 
# @File    : AutoOtaGui.py
# @Software: PyCharm
from tkinter import Frame
import tkinter as tk
from tkinter import messagebox
from Requests.AutoOta import Filter,Api

root=tk.Tk()

root.title('Auto Ota')

#左边框
# #定义左边框
# leftFrame = Frame(root, width=600, height=600)
# leftFrame.propagate(False)
# leftFrame.pack(side='left')

tk.Label(root, text="First").grid(row=0, sticky='w',padx=2,pady=2)  # 靠右
tk.Label(root, text="Second").grid(row=2, sticky='w',padx=2,pady=2)
text1=tk.Entry(root)
text1.grid(row=0,column=1,padx=2,pady=2)
text2=tk.Entry(root)
text2.grid(row=2,column=1,padx=2,pady=2)

def outCheck():
    a=text1.get()
    print(a)
tk.Button(root,text='hitme',command=outCheck).grid(row=0,column=2,sticky='w')


# 显示‘OTA URL’
# urlFrame=Frame(leftFrame,width=100,height=50)
# urlFrame.propagate(False)
# urlFrame.pack(side='left',anchor='n',padx=5,pady=5)
# text=tk.Label(urlFrame,text='OTA URL:',font = ("楷体",12))
# text.pack(expand='yes',fill='both')
# #显示输入文本框
# inputFrame=Frame(leftFrame,width=400,height=50)
# inputFrame.propagate(False)
# inputFrame.pack(side='left',anchor='n',pady=5)
# input=tk.Entry(inputFrame)
# input.pack(expand='yes',fill='x')

#获取输入url处理函数
# def getUrl():
#     url=input.get()
#
# # 显示‘Version：’
# urlFrame1=Frame(leftFrame,width=100,height=50)
# urlFrame1.propagate(False)
# urlFrame1.pack(side='left',anchor='n',padx=5,pady=5)
# text1=tk.Label(urlFrame,text='Version:',font = ("楷体",12))
# text1.pack(expand='yes',fill='both')
# #显示输入文本框
# inputFrame1=Frame(leftFrame,width=400,height=50)
# inputFrame1.propagate(False)
# inputFrame1.pack(side='left',anchor='n',pady=5)
# input1=tk.Entry(inputFrame)
# input1.pack(expand='yes',fill='x')
#
# #获取输入版本的处理函数
# def getVersion():
#     version=input1.get()
#
#
# #显示所在环境设备列表
# deviceList=[('GWSL',1),('CDSC',2),('GWFL',3)]
# v=tk.IntVar()
# for lang,num in deviceList:
#     choiceFrame=Frame(leftFrame,width=100,height=50,bg='red')
#     choiceFrame.propagate(False)
#     choiceFrame.grid(row=3,padx=5)
#     Radio=tk.Radiobutton(choiceFrame,text=lang,variable=v,value=num)
#     Radio.grid_propagate(0)
#     Radio.pack(side='left',expand='yes',fill='both')


# 右边框
# rightFrame=Frame(root,width=200,height=400,bg='blue')
# rightFrame.propagate(False)
# rightFrame.pack(side='left',padx=4)


root.mainloop()
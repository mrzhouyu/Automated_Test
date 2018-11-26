# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 18:06
# @Author  : YuChou
# @Site    : 
# @File    : CsvToExcel.py
# @Software: PyCharm
import xlwings as xw
import csv
import os
import shutil


class WriteInExcel():
    def __init__(self):
        self.TemPath = "report_temple.xlsx"
        self.CsvPath = "log.csv"
        self.Datas = self.ReadCsv()
    #读取CSV事件
    def ReadCsv(self):
        DList = []
        with open(self.CsvPath, "r", encoding="utf8", newline='') as f:
            csvFile = csv.reader(f)
            for item in csvFile:
                SList = []
                for i in item:
                    SList.append(i.strip("\t").lstrip(" ").rstrip(""))
                DList.append(SList)
        return DList

    #读取模板  格式  写入来自CSV的数据
    def ReadTem(self):
        NewName = "copy.xlsx"
        shutil.copyfile(self.TemPath,NewName)
        app = xw.App(visible=False, add_book=False)
        app.display_alerts = False
        app.screen_updating = False
        wb = app.books.open(NewName)
        sht = wb.sheets["sheet1"]
        sht.clear_contents() #只清除内容 不清除格式
        for l in range(1,len(self.Datas)+1):
            row = "A"+str(l)
            sht.range(row).value = self.Datas[l-1]
        wb.save()
        wb.close()
        app.quit()

if __name__ == "__main__":
    W = WriteInExcel()
    W.ReadTem()
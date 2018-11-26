# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 21:42
# @Author  : YuChou
# @Site    : 
# @File    : autoCreateBarcode.py
# @Software: PyCharm
from pystrich.ean13 import EAN13Encoder
from barcode.writer import ImageWriter
from barcode.ean import EuropeanArticleNumber13


def transfer(s):
    encoder=EAN13Encoder(s)
    encoder.save(s+".jpg")

transfer('6901294177017')
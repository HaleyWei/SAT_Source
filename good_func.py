# coding=utf-8
import sys
import xlrd
import os
import re
from xlutils import copy
import pickle
import httplib
from joern.all import JoernSteps
from py2neo.packages.httpstream import http
http.socket_timeout = 9999


func_list = []


def get_func(func_file):
    book = xlrd.open_workbook(func_file)
    table = book.sheet_by_name('func')
    number = 0
    for row in range(1, table.nrows):
        func_name = table.cell_value(row, 0).split(':')[1]
        res = re.findall(r'GOOD', func_name, re.I)
        if res != []:
            number += 1
    print number


def seek_file(src_path, name):
    for root, dirs, files in os.walk(src_path):
        if name in files:
            final_path = '{0}/{1}'.format(root, name)
            func_list.append(final_path)


if __name__ == '__main__':
    src_path = sys.argv[1]
    file_name = "func.xls"
    seek_file(src_path, file_name)
    for func_file in func_list:
        print func_file
        get_func(func_file)

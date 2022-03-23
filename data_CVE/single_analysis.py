# coding=utf-8
import sys
import xlrd
import xlwt
import os
import shutil
import numpy as np


path1 = "/home/wei/CWE/Desktop/ffmpeg-0.6"
# 分析程序中关键数据与总数据
path2 = "/home/wei/CWE/Desktop/openssl-1.0.1"
path1_2 = "/home/wei/CWE/Desktop/dovecot-1.2.0"
path1_3 = "/home/wei/CWE/Desktop/gzip-1.3.5"
path3 = "/home/wei/CWE/Desktop/CWE121_Stack_Based_Buffer_Overflow/s01"
path4 = "/home/wei/CWE/Desktop/spec2000/benchmark/164_gzip/src"
path5 = "/home/wei/CWE/Desktop/spec2000/benchmark/175_vpr/src"
path6 = "/home/wei/CWE/Desktop/spec2000/benchmark/179_art/src"
path7 = "/home/wei/CWE/Desktop/spec2000/benchmark/181_mcf/src"
path8 = "/home/wei/CWE/Desktop/spec2000/benchmark/183_equake/src"
path9 = "/home/wei/CWE/Desktop/spec2000/benchmark/186_crafty/src"
path10 = "/home/wei/CWE/Desktop/spec2000/benchmark/188_ammp/src"
path11 = "/home/wei/CWE/Desktop/spec2000/benchmark/197_parser/src"
path12 = "/home/wei/CWE/Desktop/spec2000/benchmark/256_bzip2/src"
path13 = "/home/wei/CWE/Desktop/spec2000/benchmark/300_twolf/src"


xtype = "xls"
name = []
typedata = []
all_var_num = 0
key_var_num = 0

key_data_num = 0
var_num = 0


################获取xls############
def collect_xls(list_collect, type1):
    # 取得列表中所有的type文件
    for each_element in list_collect:
        if isinstance(each_element, list):
            collect_xls(each_element, type1)
        elif each_element.endswith(type1):
            typedata.insert(0, each_element)
    # print(len(typedata))
    return typedata


def read_xls(path, xtype):
    global key_data_num, var_num

    all_xls = []
    for file in os.walk(path):
        for each_list in file[2]:
            file_path = file[0] + "/" + each_list
            # os.walk()函数返回三个参数：路径，子文件夹，路径下的文件，利用字符串拼接file[0]和file[2]得到文件的路径
            name.insert(0, file_path)
        all_xls = collect_xls(name, xtype)

    for evey_name in all_xls:

        xls_data = xlrd.open_workbook(evey_name)
        table1 = xls_data.sheet_by_name('pointer')
        table2 = xls_data.sheet_by_name('data')
        table3 = xls_data.sheet_by_name('define')
        table4 = xls_data.sheet_by_name('op')
        table5 = xls_data.sheet_by_name('func')
        table6 = xls_data.sheet_by_name('def_use')
        table9 = xls_data.sheet_by_name('space')
        table10 = xls_data.sheet_by_name('cond')
        table11 = xls_data.sheet_by_name('func_call')

        for row_2 in range(1, table2.nrows):
            var_num += 1
            key_data_column = table2.cell_value(row_2, 4)
            print table2.cell_value(row_2, 1)
            if key_data_column == 'key_non_control_data' or key_data_column == 'key_control_data':
                key_data_num += 1


def input_Quantitative_indicators():

    q = (float(key_data_num) / var_num) * 100
    print '所有数据数量：', var_num
    print '关键数据数量：', key_data_num
    print '占比：', '%.3f' % q + '%'


if __name__ == '__main__':
    read_xls(path13, xtype)
    input_Quantitative_indicators()

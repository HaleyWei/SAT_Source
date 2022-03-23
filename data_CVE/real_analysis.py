# coding=utf-8
import sys
import xlrd
import xlwt
import os
import shutil
import numpy as np

# 真实程序漏洞路径
path1 = "/home/wei/CWE/Desktop/ffmpeg-0.6"
path2 = "/home/wei/CWE/Desktop/openssl"

ffmpeg_list = ["libavcodec/error_resilience", "libavcodec/svq1dec", "libavcodec/aacsbr",
               "libavcodec/smc", "libavcodec/gifdec", "libavcodec/utils", "libavcodec/mjpegdec", "libavcodec/parser", "libavcodec/rpza"]
openssl_list = ["a_d2i_fp", "d1_both", "t1_lib",
                "srp_lib", "d1_lib", "dsa_ameth", "bn_print"]


def collect_xls(path):
    global path1, path2, ffmpeg_list, openssl_list

    name = "/home/wei/wanring_data.xls"
    book = xlwt.Workbook()
    collect_list = []
    if path == path1:
        for file in os.walk(path):
            for each_list in file[2]:
                if each_list.split('.')[-1] == "xls" and file[0].split("ffmpeg-0.6/")[-1] + "/" + each_list.split('.')[0] in ffmpeg_list:
                    file_path = file[0] + "/" + each_list
                    collect_list.append(file_path)
    elif path == path2:
        for file in os.walk(path):
            for each_list in file[2]:
                if each_list.split('.')[-1] == "xls" and each_list.split('.')[0] in openssl_list:
                    file_path = file[0] + "/" + each_list
                    collect_list.append(file_path)
    for every_name in collect_list:
        print every_name
        final_sheet = book.add_sheet(every_name.split('/')[-1].split('.')[0])
        final_sheet.write(0, 0, 'line')
        '''
        warning = 0
        xls_data = xlrd.open_workbook(every_name)
        table = xls_data.sheet_by_name('unsafe_op')
        for row in range(1, table.nrows):
            warning += 1
        print every_name + ":" + str(warning)
        '''
        xls_data = xlrd.open_workbook(every_name)
        table1 = xls_data.sheet_by_name('func_call')
        table2 = xls_data.sheet_by_name('unsafe_op')
        table3 = xls_data.sheet_by_name('def_use')
        table4 = xls_data.sheet_by_name('pointer')
        table5 = xls_data.sheet_by_name('op')
        table6 = xls_data.sheet_by_name('data')

        final_unsafe_op_list = []
        output_data_list = []
        final_unsafe_list = []
        warning = 0

        for row_6 in range(1, table6.nrows):
            source_data_column = table6.cell_value(row_6, 6)
            name_column = table6.cell_value(row_6, 1)
            if source_data_column == 'output':
                output_data_list.append(name_column)

        for row_1 in range(1, table1.nrows):
            line_column = table1.cell_value(row_1, 0)
            source_column = table1.cell_value(row_1, 9)
            # 用于赋值的函数语句、单独存在的函数语句
            if (source_column == 'output'):
                final_unsafe_op_list.append(line_column)

        for row_2 in range(1, table2.nrows):
            line_column = table2.cell_value(row_2, 0)
            final_unsafe_op_list.append(line_column)

        for row_3 in range(1, table3.nrows):
            line_column = table3.cell_value(row_3, 0)
            src_arg_column = table3.cell_value(row_3, 2)
            dst_arg_column = table3.cell_value(row_3, 3)
            src_column = table3.cell_value(row_3, 4)
            dst_column = table3.cell_value(row_3, 5)
            src_list = list(set(src_column.split(' ')))
            dst_list = list(set(dst_column.split(' ')))

            for row_4 in range(1, table4.nrows):
                name_column = table4.cell_value(row_4, 1)
                key_data_column = table4.cell_value(row_4, 9)

                if name_column in src_arg_column.split(' '):
                    if key_data_column is not 'normal':
                        for sl in src_list:
                            for row_5 in range(1, table5.nrows):
                                line_column5 = table5.cell_value(row_5, 0)
                                src_column5 = table5.cell_value(row_5, 3)
                                if sl == line_column5:
                                    for s_c in src_column5.split(' '):
                                        if s_c in output_data_list:
                                            final_unsafe_op_list.append(
                                                line_column5)

        final_unsafe_op_list = list(set(final_unsafe_op_list))
        for unsafe_op in final_unsafe_op_list:
            final_unsafe_list.append(int(unsafe_op))

        final_unsafe_list.sort()
        for unsafe_op in final_unsafe_list:
            warning += 1
            final_sheet.write(warning, 0, unsafe_op)

        print warning
    book.save(name)


if __name__ == '__main__':
    collect_xls(path1)

# coding=utf-8
import sys
import xlrd
import xlwt
import os
import sys
from xlutils import copy


class unsafe_pointer:
    def __init__(self, line, ptr_name, unsafe_ptr_reason, unsafe_line):
        self.line = line
        self.ptr_name = ptr_name
        self.unsafe_ptr_reason = unsafe_ptr_reason
        self.unsafe_line = unsafe_line


xtype = "xls"
name = []
typedata = []
file_path = []


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
    # 遍历路径文件夹
    all_xls = []

    for file in os.walk(path):
        for each_list in file[2]:
            if each_list.split('.')[-1] == "xls":
                xls_name = file[0] + '/' + each_list
                all_xls.append(xls_name)

    '''
    for file in os.walk(path):
        for each_list in file[2]:
            if(each_list.endswith(".result.xls")):
                os.remove(os.path.join(file[0], each_list))
                continue
            file_path = file[0] + "/" + each_list
            # os.walk()函数返回三个参数：路径，子文件夹，路径下的文件，利用字符串拼接file[0]和file[2]得到文件的路径
            name.insert(0, file_path)
        all_xls = collect_xls(name, xtype)
    '''

    for evey_name in all_xls:
        xls_data = xlrd.open_workbook(evey_name)
        if 'unsafe_pointer' in xls_data.sheet_names():
            continue
        wb = copy.copy(xls_data)
        sheet_1 = wb.add_sheet('unsafe_pointer')
        sheet_1.write(0, 0, 'line')
        sheet_1.write(0, 1, 'ptr_name')
        sheet_1.write(0, 2, 'unsafe_ptr_reason')
        sheet_1.write(0, 3, 'unsafe_line')
        index_excle = 1
        unsafe_pointer_excle = []
        print evey_name
        table1 = xls_data.sheet_by_name('pointer')
        table2 = xls_data.sheet_by_name('def_use')
        table3 = xls_data.sheet_by_name('op')
        table4 = xls_data.sheet_by_name('func_call')
        print "单行分析"
        single_line = []
        pointer_table = []
        for row in range(1, table1.nrows):
            pointer_table.append(table1.cell_value(row, 1))
            if table1.cell_value(row, 2) == "unsafe":
                pointer_line = table1.cell_value(row, 0)
                pointer_name = table1.cell_value(row, 1)
                pointer_unsafe_line = table1.cell_value(row, 5)
                pointer_unsafe_reason = table1.cell_value(row, 4)
                a = unsafe_pointer(pointer_line, pointer_name,
                                   pointer_unsafe_reason, pointer_unsafe_line)
                unsafe_pointer_excle.append(a)
                single_line.append(pointer_name)

        print "多行分析"
        multi_line = []
        for row in range(1, table2.nrows):
            if table2.cell_value(row, 1) == "op":
                flag = 0
                for arg in table2.cell_value(row, 2).split(' '):
                    if arg in single_line:
                        flag = 1
                if flag == 1:
                    for arg in table2.cell_value(row, 3).split(' '):
                        if arg in pointer_table:
                            for point in range(1, table1.nrows):
                                if arg == table1.cell_value(point, 1):
                                    pointer_line = table1.cell_value(point, 0)
                                    pointer_name = table1.cell_value(point, 1)
                                    pointer_unsafe_line = table1.cell_value(
                                        point, 5) + table2.cell_value(row, 0)
                                    pointer_unsafe_reason = table1.cell_value(
                                        point, 4) + "unsafe_ptr_to_ptr "
                                    a = unsafe_pointer(
                                        pointer_line, pointer_name, pointer_unsafe_reason, pointer_unsafe_line)
                                    for i in unsafe_pointer_excle:
                                        if i.line == a.line and i.ptr_name == a.ptr_name:
                                            unsafe_pointer_excle.remove(i)
                                    unsafe_pointer_excle.append(a)

        for it in unsafe_pointer_excle:
            sheet_1.write(index_excle, 0, it.line)
            sheet_1.write(index_excle, 1, it.ptr_name)
            sheet_1.write(index_excle, 2, it.unsafe_ptr_reason)
            sheet_1.write(index_excle, 3, it.unsafe_line)
            index_excle += 1
        wb.save(evey_name)


if __name__ == '__main__':
    src_path = sys.argv[1]
    path = "/home/weihaolai/ICKD_analysis/data_CVE/" + src_path + "/code"
    read_xls(path, xtype)

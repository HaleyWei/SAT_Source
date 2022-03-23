# coding=utf-8
import sys
import xlrd
import xlwt
import os
import sys
from xlutils import copy


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
        wb = copy.copy(xls_data)

        table1 = xls_data.sheet_by_name('pointer')
        table2 = xls_data.sheet_by_name('data')

        sheet_1 = wb.get_sheet('pointer')

        for row in range(1, table1.nrows):
            appear_line_list = ""
            for code_line in table1.cell_value(row, 3).split(','):
                appear_line_list += code_line.split('@')[0] + " "
            safety = table1.cell_value(row, 2)
            unsafe_reason = table1.cell_value(row, 4)
            unsafe_line = table1.cell_value(row, 5)

            pointer_name = table1.cell_value(row, 1).split('@')[0]
            point_name = "* " + pointer_name
            func_name = table1.cell_value(row, 1).split('@')[-1]
            for code_line in table1.cell_value(row, 3).split(','):
                code = code_line.split('@')[-1]
                line = code_line.split('@')[0]
                if code.find('=') != -1:
                    if (pointer_name in code.split('=')[0].split(' ')) and (point_name not in str(code.split('=')[0])):
                        for data_row in range(1, table2.nrows):
                            if table2.cell_value(data_row, 1).split('@')[-1] == func_name and table2.cell_value(data_row, 1).split('@')[0] in code.split('=')[-1].split(' '):
                                print "have"
                                if table2.cell_value(data_row, 6) == "output":
                                    unsafe_line += line + " "
                                    safety = "unsafe"
                                    unsafe_reason += "out_to_ptr "
                                if table2.cell_value(data_row, 5) == "stack_loc":
                                    unsafe_line += line + " "
                                    safety = "unsafe"
                                    unsafe_reason += "stack_to_ptr "
                if code.find(' + ') != -1:
                    if (pointer_name in code.split(' + ')[0].split(' ')) and (point_name not in str(code.split(' + ')[0])):
                        for data_row in range(1, table2.nrows):
                            if table2.cell_value(data_row, 1).split('@')[-1] == func_name and table2.cell_value(data_row, 1).split('@')[0] in code.split(' + ')[-1].split(' '):
                                unsafe_line += line + " "
                                safety = "unsafe"
                                unsafe_reason += "offset_is_var "
                                if table2.cell_value(data_row, 6) == "output":
                                    unsafe_line += line + " "
                                    safety = "unsafe"
                                    unsafe_reason += "offset_is_output "
                if code.find(' - ') != -1:
                    if (pointer_name in code.split(' - ')[0].split(' ')) and (point_name not in str(code.split(' - ')[0])):
                        for data_row in range(1, table2.nrows):
                            if table2.cell_value(data_row, 1).split('@')[-1] == func_name and table2.cell_value(data_row, 1).split('@')[0] in code.split(' - ')[-1].split(' '):
                                unsafe_line += line + " "
                                safety = "unsafe"
                                unsafe_reason += "offset_is_var "
                                if table2.cell_value(data_row, 6) == "output":
                                    unsafe_line += line + " "
                                    safety = "unsafe"
                                    unsafe_reason += "offset_is_output "

            sheet_1.write(row, 3, appear_line_list)
            sheet_1.write(row, 2, safety)
            sheet_1.write(row, 4, unsafe_reason)
            sheet_1.write(row, 5, unsafe_line)

            wb.save(evey_name)


if __name__ == '__main__':
    src_path = sys.argv[1]
    path = "/home/weihaolai/ICKD_analysis/data_CVE/" + src_path + "/code"
    read_xls(path, xtype)

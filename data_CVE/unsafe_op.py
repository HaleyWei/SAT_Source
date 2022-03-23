# coding=utf-8
import sys
import xlrd
import xlwt
import os
import sys
from xlutils import copy


class unsafe_op:
    def __init__(self, line, state_type, func_name, is_readorwrite, safety, unsafe_op_reason):
        self.line = line
        self.state_type = state_type
        self.func_name = func_name
        self.is_readorwrite = is_readorwrite
        self.safety = safety
        self.unsafe_op_reason = unsafe_op_reason


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
        if 'unsafe_op' in xls_data.sheet_names():
            continue
        wb = copy.copy(xls_data)

        sheet_1 = wb.add_sheet('unsafe_op')
        sheet_1.write(0, 0, 'line')
        sheet_1.write(0, 1, 'state_type')
        sheet_1.write(0, 2, 'func_name')
        sheet_1.write(0, 3, 'is_readorwrite')
        sheet_1.write(0, 4, 'safety')
        sheet_1.write(0, 5, 'unsafe_op_reason')
        index_excle = 1
        unsafe_op_excle = []
        unsafe_func_excle = []
        print evey_name
        table1 = xls_data.sheet_by_name('unsafe_pointer')
        table2 = xls_data.sheet_by_name('op')
        table3 = xls_data.sheet_by_name('func_call')
        table4 = xls_data.sheet_by_name('func')
        table5 = xls_data.sheet_by_name('data')
        table6 = xls_data.sheet_by_name('cond')
        sheet_2 = wb.get_sheet('op')
        sheet_3 = wb.get_sheet('func_call')
        # 2020.8.23+ 函数调用的输入类型
        sheet_3.write(0, 9, 'source')

        for row in range(1, table2.nrows):
            op_line = table2.cell_value(row, 0)
            op_state_type = table2.cell_value(row, 2)
            op_func_name = table2.cell_value(row, 1)
            op_is_readorwrite = table2.cell_value(row, 5)
            op_safety = ""
            op_unsafe_reason = ""
            if table2.cell_value(row, 3):
                for src_arg in table2.cell_value(row, 3).split(' '):
                    if src_arg and src_arg.split('@')[-1] != "global":
                        for data_row in range(1, table5.nrows):
                            if src_arg == table5.cell_value(data_row, 1):
                                if table5.cell_value(data_row, 4) == "key_non_control_data":
                                    op_safety += "non_control_data"
                                elif table5.cell_value(data_row, 4) == "key_control_data":
                                    op_safety += "control_data"
                                elif table5.cell_value(data_row, 4) == "normal":
                                    op_safety += "normal"
                                flag = 0
                                for point_row in range(1, table1.nrows):
                                    if src_arg == table1.cell_value(point_row, 1) and op_line in table1.cell_value(point_row, 3).split(' '):
                                        flag = 1
                                if flag == 1:
                                    op_safety += "_unsafe"
                                else:
                                    op_safety += "_safe"
                                op_safety += "_read "
            if table2.cell_value(row, 4):
                for dst_arg in table2.cell_value(row, 4).split(' '):
                    if dst_arg and dst_arg.split('@')[-1] != "global":
                        for data_row in range(1, table5.nrows):
                            if dst_arg == table5.cell_value(data_row, 1):
                                if table5.cell_value(data_row, 4) == "key_non_control_data":
                                    op_safety += "non_control_data"
                                elif table5.cell_value(data_row, 4) == "key_control_data":
                                    op_safety += "control_data"
                                elif table5.cell_value(data_row, 4) == "normal":
                                    op_safety += "normal"
                                flag = 0
                                for point_row in range(1, table1.nrows):
                                    if dst_arg == table1.cell_value(point_row, 1) and op_line in table1.cell_value(point_row, 3).split(' '):
                                        flag = 1
                                if flag == 1:
                                    op_safety += "_unsafe"
                                else:
                                    op_safety += "_safe"
                                op_safety += "_write "
            for point_row in range(1, table1.nrows):
                flag = 0
                for line in table1.cell_value(point_row, 3).split(' '):
                    if op_line == line:
                        reason = table1.cell_value(point_row, 2).split(' ')
                        op_unsafe_reason += reason[flag] + " "
                    print flag
                    print line
                    flag += 1

            sheet_2.write(row, 6, op_safety)
            sheet_2.write(row, 7, op_unsafe_reason)
            a = unsafe_op(op_line, op_state_type, op_func_name,
                          op_is_readorwrite, op_safety, op_unsafe_reason)
            unsafe_op_excle.append(a)

        for row in range(1, table3.nrows):
            op_line = table3.cell_value(row, 0)
            op_state_type = table3.cell_value(row, 1)
            op_func_name = table3.cell_value(row, 2)
            op_is_readorwrite = table3.cell_value(row, 6)
            op_safety = ""
            op_unsafe_reason_1 = ""
            op_unsafe_reason_2 = ""
            for func_row in range(1, table4.nrows):
                if table3.cell_value(row, 5) == table4.cell_value(func_row, 0):
                    for point_row in range(1, table1.nrows):
                        flag = 0
                        for line in table1.cell_value(point_row, 3).split(' '):
                            if line and table4.cell_value(func_row, 3) and table4.cell_value(func_row, 4):
                                if int(line) >= int(table4.cell_value(func_row, 3)) and int(line) <= int(table4.cell_value(func_row, 4)):
                                    reason = table1.cell_value(
                                        point_row, 2).split(' ')
                                    op_unsafe_reason_1 += reason[flag] + " "
                            flag += 1
            # 2020.8.25+ 少统计了一种情况，只考虑了调用函数存在非安全操作的情况，没考率非安全操作本身
            for point_row in range(1, table1.nrows):
                flag = 0
                for line in table1.cell_value(point_row, 3).split(' '):
                    if line:
                        if int(line) == int(op_line):
                            reason = table1.cell_value(point_row, 2).split(' ')
                            op_unsafe_reason_2 += reason[flag] + " "
                    flag += 1
            # 2020.8.22+ 判断函数调用语句位置与条件判断语句是否相等，若不等则为输入
            flag = 0
            for row_6 in range(1, table6.nrows):
                if table6.cell_value(row_6, 0) == table3.cell_value(row, 0):
                    flag = 1
            if flag == 0:
                sheet_3.write(row, 9, 'output')

            if op_unsafe_reason_1:
                sheet_3.write(row, 8, op_unsafe_reason_1)
            elif op_unsafe_reason_2:
                sheet_3.write(row, 8, op_unsafe_reason_2)
                a = unsafe_op(op_line, op_state_type, op_func_name,
                              op_is_readorwrite, op_safety, op_unsafe_reason_2)
                unsafe_func_excle.append(a)

        unsafe_op_func_excle = []
        op_excle = unsafe_op_excle
        func_excle = unsafe_func_excle
        for line_1 in unsafe_op_excle:
            for line_2 in unsafe_func_excle:
                if line_1.line == line_2.line:
                    state_type = line_1.state_type + " " + line_2.state_type
                    unsafe_op_reason = line_1.unsafe_op_reason + line_2.unsafe_op_reason
                    a = unsafe_op(line_1.line, state_type, line_1.func_name,
                                  line_1.is_readorwrite, line_1.safety, unsafe_op_reason)
                    print line_1.line + 'hhhh'
                    print a.line + 'hhhh'
                    if line_1 in op_excle:
                        op_excle.remove(line_1)
                        func_excle.remove(line_2)
                        op_excle.append(a)

        unsafe_op_func_excle = op_excle + func_excle
        # 2020.8.29+ 统计非安全操作行号，防止有遗漏的非安全操作
        unsafe_line = []
        for it in unsafe_op_func_excle:
            if it.unsafe_op_reason:
                unsafe_line.append(it.line)
        for point_row in range(1, table1.nrows):
            flag = 0
            for point_line in table1.cell_value(point_row, 3).split(' '):
                if point_line:
                    if point_line not in unsafe_line:
                        n = table1.cell_value(point_row, 1).split('@')[-1]
                        r = table1.cell_value(point_row, 2).split(' ')[flag]
                        a = unsafe_op(point_line, "", n, "", "", r)
                        unsafe_line.append(point_line)
                        unsafe_op_func_excle.append(a)
                flag += 1
        for it in unsafe_op_func_excle:
            if it.unsafe_op_reason:
                sheet_1.write(index_excle, 0, it.line)
                sheet_1.write(index_excle, 1, it.state_type)
                sheet_1.write(index_excle, 2, it.func_name)
                sheet_1.write(index_excle, 3, it.is_readorwrite)
                sheet_1.write(index_excle, 4, it.safety)
                sheet_1.write(index_excle, 5, it.unsafe_op_reason)
                index_excle += 1
        wb.save(evey_name)


if __name__ == '__main__':
    src_path = sys.argv[1]
    path = "/home/weihaolai/ICKD_analysis/data_CVE/" + src_path + "/code"
    read_xls(path, xtype)

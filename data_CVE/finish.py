import xlrd
import xlwt
import sys


def file_opera(src_path, pointer_file, data_file, define_file, op_file, func_file, defuse_file, space_file, cond_file, funccall_file):

    book_1 = xlrd.open_workbook(pointer_file)
    book_2 = xlrd.open_workbook(data_file)
    book_3 = xlrd.open_workbook(define_file)
    book_4 = xlrd.open_workbook(op_file)
    book_5 = xlrd.open_workbook(func_file)
    book_6 = xlrd.open_workbook(defuse_file)
    book_7 = xlrd.open_workbook(space_file)
    book_8 = xlrd.open_workbook(cond_file)
    book_9 = xlrd.open_workbook(funccall_file)
    sheet_1 = book_1.sheet_by_index(1)
    sheet_2 = book_2.sheet_by_index(1)
    sheet_3 = book_3.sheet_by_index(1)
    sheet_4 = book_4.sheet_by_index(1)
    sheet_5 = book_5.sheet_by_index(1)
    sheet_6 = book_6.sheet_by_index(1)
    sheet_7 = book_7.sheet_by_index(0)
    sheet_8 = book_8.sheet_by_index(0)
    sheet_9 = book_9.sheet_by_index(0)
    file_list = []
    col_1 = sheet_1.col_values(0)
    col_2 = sheet_2.col_values(0)
    col_3 = sheet_3.col_values(0)
    col_4 = sheet_4.col_values(0)
    col_5 = sheet_5.col_values(0)
    col_6 = sheet_6.col_values(0)
    col_7 = sheet_7.col_values(0)
    col_8 = sheet_8.col_values(0)
    col_9 = sheet_9.col_values(0)

    split_line = src_path + '/'

    for col in col_1[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_2[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_3[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_4[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_5[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_6[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_7[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_8[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)
    for col in col_9[1:]:
        if col.split(':')[0].split('.')[-1] != 'h':
            file_name = col.split(':')[0].split(split_line)[-1].split('.')[0]
            if file_name not in file_list:
                file_list.append(file_name)

    for file in file_list:
        print file
        index = [1, 1, 1, 1, 1, 1, 1, 1, 1]

        name = "/home/weihaolai/ICKD_analysis/data_CVE/" + \
            split_line + "code/" + file + ".xls"
        book = xlwt.Workbook()
        final_sheet_1 = book.add_sheet('pointer')
        final_sheet_2 = book.add_sheet('data')
        final_sheet_3 = book.add_sheet('define')
        final_sheet_4 = book.add_sheet('op')
        final_sheet_5 = book.add_sheet('func')
        final_sheet_6 = book.add_sheet('def_use')
        final_sheet_7 = book.add_sheet('space')
        final_sheet_8 = book.add_sheet('cond')
        final_sheet_9 = book.add_sheet('func_call')
        final_sheet_1.write(0, 0, 'line')
        final_sheet_1.write(0, 1, 'name')
        final_sheet_1.write(0, 2, 'safety')
        final_sheet_1.write(0, 3, 'appear_line')
        final_sheet_1.write(0, 4, 'unsafe_reason')
        final_sheet_1.write(0, 5, 'unsafe_line')
        final_sheet_1.write(0, 6, 'loc')
        final_sheet_1.write(0, 7, 'pointer_type')
        final_sheet_1.write(0, 8, 'point_to')
        final_sheet_1.write(0, 9, 'key_data')
        final_sheet_1.write(0, 10, 'scope')
        final_sheet_1.write(0, 11, 'pointer_range')
        final_sheet_2.write(0, 0, 'line')
        final_sheet_2.write(0, 1, 'name')
        final_sheet_2.write(0, 2, 'data_type')
        final_sheet_2.write(0, 3, 'data_content')
        final_sheet_2.write(0, 4, 'key_data')
        final_sheet_2.write(0, 5, 'loc')
        final_sheet_2.write(0, 6, 'source')
        final_sheet_2.write(0, 7, 'status')
        final_sheet_2.write(0, 8, 'scope')
        final_sheet_2.write(0, 9, 'data_use')
        final_sheet_3.write(0, 0, 'line')
        final_sheet_3.write(0, 1, 'func_name')
        final_sheet_3.write(0, 2, 'state_type')
        final_sheet_3.write(0, 3, 'arg')
        final_sheet_4.write(0, 0, 'line')
        final_sheet_4.write(0, 1, 'func_name')
        final_sheet_4.write(0, 2, 'state_type')
        final_sheet_4.write(0, 3, 'src')
        final_sheet_4.write(0, 4, 'dst')
        final_sheet_4.write(0, 5, 'is_readorwrite')
        final_sheet_4.write(0, 6, 'safety')
        final_sheet_4.write(0, 7, 'unsafe_reason')
        final_sheet_5.write(0, 0, 'func_name')
        final_sheet_5.write(0, 1, 'func_type')
        final_sheet_5.write(0, 2, 'func_arg')
        final_sheet_5.write(0, 3, 'start_line')
        final_sheet_5.write(0, 4, 'finish_line')
        final_sheet_6.write(0, 0, 'line')
        final_sheet_6.write(0, 1, 'state_type')
        final_sheet_6.write(0, 2, 'src_arg')
        final_sheet_6.write(0, 3, 'dst_arg')
        final_sheet_6.write(0, 4, 'src')
        final_sheet_6.write(0, 5, 'dst')
        final_sheet_7.write(0, 0, 'line')
        final_sheet_7.write(0, 1, 'func_name')
        final_sheet_7.write(0, 2, 'space_name')
        final_sheet_7.write(0, 3, 'space_type')
        final_sheet_7.write(0, 4, 'loc')
        final_sheet_7.write(0, 5, 'space_size')
        final_sheet_8.write(0, 0, 'line')
        final_sheet_8.write(0, 1, 'state_type')
        final_sheet_8.write(0, 2, 'func_name')
        final_sheet_8.write(0, 3, 'arg')
        final_sheet_8.write(0, 4, 'type')
        final_sheet_8.write(0, 5, 'start_line')
        final_sheet_8.write(0, 6, 'end_line')
        final_sheet_9.write(0, 0, 'line')
        final_sheet_9.write(0, 1, 'state_type')
        final_sheet_9.write(0, 2, 'func_name')
        final_sheet_9.write(0, 3, 'call_type')
        final_sheet_9.write(0, 4, 'func_arg')
        final_sheet_9.write(0, 5, 'func_called_name')
        final_sheet_9.write(0, 6, 'is_readorwrite')
        final_sheet_9.write(0, 7, 'safety')
        final_sheet_9.write(0, 8, 'unsafe_reason')

        for row in range(1, sheet_1.nrows):
            if sheet_1.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_1.write(
                    index[0], 0, sheet_1.row_values(row)[0].split(':')[1])
                final_sheet_1.write(index[0], 1, sheet_1.row_values(row)[1])
                final_sheet_1.write(index[0], 2, sheet_1.row_values(row)[2])
                final_sheet_1.write(index[0], 3, sheet_1.row_values(row)[3])
                final_sheet_1.write(index[0], 4, sheet_1.row_values(row)[4])
                final_sheet_1.write(index[0], 5, sheet_1.row_values(row)[5])
                final_sheet_1.write(index[0], 6, sheet_1.row_values(row)[6])
                final_sheet_1.write(index[0], 7, sheet_1.row_values(row)[7])
                final_sheet_1.write(index[0], 8, sheet_1.row_values(row)[8])
                final_sheet_1.write(index[0], 9, sheet_1.row_values(row)[9])
                final_sheet_1.write(index[0], 10, sheet_1.row_values(row)[10])
                final_sheet_1.write(index[0], 11, sheet_1.row_values(row)[11])
                index[0] += 1

        for row in range(1, sheet_2.nrows):
            if sheet_2.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_2.write(
                    index[1], 0, sheet_2.row_values(row)[0].split(':')[1])
                final_sheet_2.write(index[1], 1, sheet_2.row_values(row)[1])
                final_sheet_2.write(index[1], 2, sheet_2.row_values(row)[2])
                final_sheet_2.write(index[1], 3, sheet_2.row_values(row)[3])
                final_sheet_2.write(index[1], 4, sheet_2.row_values(row)[4])
                final_sheet_2.write(index[1], 5, sheet_2.row_values(row)[5])
                final_sheet_2.write(index[1], 6, sheet_2.row_values(row)[6])
                final_sheet_2.write(index[1], 7, sheet_2.row_values(row)[7])
                final_sheet_2.write(index[1], 8, sheet_2.row_values(row)[8])
                final_sheet_2.write(index[1], 9, sheet_2.row_values(row)[9])
                index[1] += 1

        for row in range(1, sheet_3.nrows):
            if sheet_3.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file and sheet_3.row_values(row)[2] == "define":
                final_sheet_3.write(
                    index[2], 0, sheet_3.row_values(row)[0].split(':')[1])
                final_sheet_3.write(index[2], 1, sheet_3.row_values(row)[1])
                final_sheet_3.write(index[2], 2, sheet_3.row_values(row)[2])
                final_sheet_3.write(index[2], 3, sheet_3.row_values(row)[3])
                index[2] += 1

        for row in range(1, sheet_4.nrows):
            if sheet_4.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_4.write(
                    index[3], 0, sheet_4.row_values(row)[0].split(':')[1])
                final_sheet_4.write(index[3], 1, sheet_4.row_values(row)[1])
                final_sheet_4.write(index[3], 2, sheet_4.row_values(row)[2])
                final_sheet_4.write(index[3], 3, sheet_4.row_values(row)[3])
                final_sheet_4.write(index[3], 4, sheet_4.row_values(row)[4])
                final_sheet_4.write(index[3], 5, sheet_4.row_values(row)[5])
                final_sheet_4.write(index[3], 6, sheet_4.row_values(row)[6])
                final_sheet_4.write(index[3], 7, sheet_4.row_values(row)[7])
                index[3] += 1

        for row in range(1, sheet_5.nrows):
            if sheet_5.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_5.write(
                    index[4], 0, sheet_5.row_values(row)[0].split(':')[1])
                final_sheet_5.write(index[4], 1, sheet_5.row_values(row)[1])
                final_sheet_5.write(index[4], 2, sheet_5.row_values(row)[2])
                final_sheet_5.write(index[4], 3, sheet_5.row_values(row)[3])
                final_sheet_5.write(index[4], 4, sheet_5.row_values(row)[4])
                index[4] += 1

        for row in range(1, sheet_6.nrows):
            if sheet_6.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_6.write(
                    index[5], 0, sheet_6.row_values(row)[0].split(':')[-1])
                final_sheet_6.write(index[5], 1, sheet_6.row_values(row)[1])
                final_sheet_6.write(index[5], 2, sheet_6.row_values(row)[2])
                final_sheet_6.write(index[5], 3, sheet_6.row_values(row)[3])
                final_sheet_6.write(index[5], 4, sheet_6.row_values(row)[4])
                final_sheet_6.write(index[5], 5, sheet_6.row_values(row)[5])
                index[5] += 1

        for row in range(1, sheet_7.nrows):
            if sheet_7.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_7.write(
                    index[6], 0, sheet_7.row_values(row)[0].split(':')[1])
                final_sheet_7.write(index[6], 1, sheet_7.row_values(row)[1])
                final_sheet_7.write(index[6], 2, sheet_7.row_values(row)[2])
                final_sheet_7.write(index[6], 3, sheet_7.row_values(row)[3])
                final_sheet_7.write(index[6], 4, sheet_7.row_values(row)[4])
                final_sheet_7.write(index[6], 5, sheet_7.row_values(row)[5])
                index[6] += 1

        for row in range(1, sheet_8.nrows):
            if sheet_8.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_8.write(
                    index[7], 0, sheet_8.row_values(row)[0].split(':')[1])
                final_sheet_8.write(index[7], 1, sheet_8.row_values(row)[1])
                final_sheet_8.write(index[7], 2, sheet_8.row_values(row)[2])
                final_sheet_8.write(index[7], 3, sheet_8.row_values(row)[3])
                final_sheet_8.write(index[7], 4, sheet_8.row_values(row)[4])
                final_sheet_8.write(index[7], 5, sheet_8.row_values(row)[5])
                final_sheet_8.write(index[7], 6, sheet_8.row_values(row)[6])
                index[7] += 1

        for row in range(1, sheet_9.nrows):
            if sheet_9.row_values(row)[0].split(':')[0].split(split_line)[-1].split('.')[0] == file:
                final_sheet_9.write(
                    index[8], 0, sheet_9.row_values(row)[0].split(':')[1])
                final_sheet_9.write(index[8], 1, sheet_9.row_values(row)[1])
                final_sheet_9.write(index[8], 2, sheet_9.row_values(row)[2])
                final_sheet_9.write(index[8], 3, sheet_9.row_values(row)[3])
                final_sheet_9.write(index[8], 4, sheet_9.row_values(row)[4])
                final_sheet_9.write(index[8], 5, sheet_9.row_values(row)[5])
                final_sheet_9.write(index[8], 6, sheet_9.row_values(row)[6])
                final_sheet_9.write(index[8], 7, sheet_9.row_values(row)[7])
                final_sheet_9.write(index[8], 8, sheet_9.row_values(row)[8])
                index[8] += 1

        book.save(name)


if __name__ == '__main__':
    src_path = sys.argv[1]
    pointer_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/pointer.xls"
    data_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/data.xls"
    define_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/define.xls"
    op_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/op.xls"
    func_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/func.xls"
    defuse_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/def_use.xls"
    space_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/space.xls"
    cond_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + src_path + "/cond.xls"
    funccall_file = "/home/weihaolai/ICKD_analysis/creat_form/data/" + \
        src_path + "/func_call.xls"

    file_opera(src_path, pointer_file, data_file, define_file, op_file,
               func_file, defuse_file, space_file, cond_file, funccall_file)

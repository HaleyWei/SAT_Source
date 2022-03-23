import xlrd
from xlutils.copy import copy
import sys


def get_array_size(str):
    import re
    size_patt = r'[[](.*?)[]]'
    size_pattern = re.compile(size_patt)
    size_num = size_pattern.findall(str)
    type_patt = r'[A-Za-z]+'
    type_pattern = re.compile(type_patt)
    type_str = type_pattern.findall(str)
    size = ""
    if len(size_num) == 1:
        if(size_num[0] == " "):
            return ""
        size = type_str[0] + "*" + size_num[0] + ""
        return size
    elif len(size_num) > 1:
        size = type_str[0]
        for size_item in size_num:
            if(size_item == " "):
                return ""
            size += "*" + size_item + ""
        return size
    else:
        return ""


def get_array_list(data_path):
    array_list = []
    data_book = xlrd.open_workbook(data_path)
    data_table = data_book.sheet_by_name("data")
    for row in range(1, data_table.nrows):
        data_item = data_table.row_values(row)
        array_size = get_array_size(data_item[2])
        if(array_size == ""):
            continue
        array_line = data_item[0]
        func_name = data_item[1].split("@")[1]
        array_name = "array@" + data_item[0].split(":")[1]
        space_type = "array_space"
        loc = "stack_loc"
        array_item = (array_line, func_name, array_name,
                      space_type, loc, array_size)

        array_list.append(array_item)
    return array_list


def add_item_to_excel(array_list, space_path):
    space_book = xlrd.open_workbook(space_path)
    new_book = copy(space_book)
    space_sheet = space_book.sheet_by_name("space")
    new_sheet = new_book.get_sheet(1)

    row = space_sheet.nrows

    for i in range(row, row + len(array_list)):
        column = 0
        for array_item in array_list[i - row]:
            new_sheet.write(i, column, array_item)
            column += 1
    new_book.save(space_path)


if __name__ == '__main__':
    src_path = sys.argv[1]
    space_path = "data/" + src_path + "/space.xls"
    data_path = "data/" + src_path + "/data.xls"
    print data_path
    array_list = get_array_list(data_path)

    add_item_to_excel(array_list, space_path)

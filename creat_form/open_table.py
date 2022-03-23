import xlwt
import xlrd


class func_call:
    def __init__(self, file, line, call_name, call_type, arg, func_name):
        self.file = file
        self.line = line
        self.call_name = call_name
        self.call_type = call_type
        self.arg = arg
        self.func_name = func_name


class cond:
    def __init__(self, file, line, arg, func_name):
        self.file = file
        self.line = line
        self.arg = arg
        self.func_name = func_name


class data_var:
    def __init__(self, file, line, name, source, loc, key_data, func_name):
        self.file = file
        self.line = line
        self.name = name
        self.source = source
        self.loc = loc
        self.key_data = key_data
        self.func_name = func_name


class pointer_var:
    def __init__(self, file, line, name, safety, unsafe_line, unsafe_reason, key_data, func_name):
        self.file = file
        self.line = line
        self.name = name
        self.safety = safety
        self.unsafe_line = unsafe_line
        self.unsafe_reason = unsafe_reason
        self.key_data = key_data
        self.func_name = func_name


class space:
    def __init__(self, file, line, space_size, func_name):
        self.file = file
        self.line = line
        self.func_name = func_name
        self.space_size = space_size


bof_func = ['strcpy', 'strcat', 'sprintf', 'vcprinty', 'scanf', 'vscanf', 'sscanf', 'vsscanf', 'fscanf', 'vfscanf',
            'strncpy', 'snprintf', 'vsnprintf', 'strncat', 'fgets', 'fread', 'read', 'memcpy', 'memmove', 'memset']


def get_func_call_table(src_path):
    funcall_workbook = xlrd.open_workbook(
        "data/" + src_path + "/func_call.xls")
    funcall_sheet = funcall_workbook.sheet_by_name("func_call")
    funcall_row = funcall_sheet.nrows
    funcall_elem = []
    for row in range(1, funcall_row):
        call_file = ""
        call_line = ""
        call_name = ""
        call_type = ""
        call_arg = []
        func_name = ""
        call_file = funcall_sheet.cell_value(
            row, 0).split('/')[-1].split(':')[0]
        call_line = funcall_sheet.cell_value(row, 0).split(':')[-1]
        call_name = funcall_sheet.cell_value(row, 5)
        call_type = funcall_sheet.cell_value(row, 3)
        if funcall_sheet.cell_value(row, 4):
            if funcall_sheet.cell_value(row, 4)[0] == '[' and funcall_sheet.cell_value(row, 4)[-1] == ']':
                call_arg = eval(funcall_sheet.cell_value(row, 4))
            else:
                call_arg.append(funcall_sheet.cell_value(row, 4))
        func_name = funcall_sheet.cell_value(row, 2)
        '''
        print call_file
        print call_line
        print call_name
        print call_type
        print call_arg
        print func_name
        '''
        a = func_call(call_file, call_line, call_name,
                      call_type, call_arg, func_name)
        funcall_elem.append(a)
    return funcall_elem


def get_cond_table(src_path):
    cond_workbook = xlrd.open_workbook("data/" + src_path + "/cond.xls")
    cond_sheet = cond_workbook.sheet_by_name("cond")
    cond_row = cond_sheet.nrows
    cond_elem = []
    for row in range(1, cond_row):
        cond_file = ""
        cond_line = ""
        cond_arg = []
        func_name = ""
        cond_file = cond_sheet.cell_value(row, 0).split('/')[-1].split(':')[0]
        cond_line = cond_sheet.cell_value(row, 0).split(':')[-1]
        if cond_sheet.cell_value(row, 3):
            if cond_sheet.cell_value(row, 3)[0] == '[' and cond_sheet.cell_value(row, 3)[-1] == ']':
                cond_arg = eval(cond_sheet.cell_value(row, 3))
            else:
                cond_arg.append(cond_sheet.cell_value(row, 3))
        func_name = cond_sheet.cell_value(row, 2)
        print cond_file
        print cond_line
        print cond_arg
        print func_name
        a = cond(cond_file, cond_line, cond_arg, func_name)
        cond_elem.append(a)
    return cond_elem


def get_data_table(src_path):
    data_workbook = xlrd.open_workbook("data/" + src_path + "/data.xls")
    data_sheet = data_workbook.sheet_by_name("data")
    data_row = data_sheet.nrows
    data_elem = []
    for row in range(1, data_row):
        data_file = ""
        data_line = ""
        data_name = ""
        data_source = ""
        data_loc = ""
        key_data = ""
        func_name = ""
        data_file = data_sheet.cell_value(row, 0).split('/')[-1].split(':')[0]
        data_line = data_sheet.cell_value(row, 0).split(':')[-1]
        data_name = data_sheet.cell_value(row, 1).split('@')[0]
        data_source = data_sheet.cell_value(row, 6)
        data_loc = data_sheet.cell_value(row, 5)
        key_data = data_sheet.cell_value(row, 4)
        func_name = data_sheet.cell_value(row, 1).split('@')[-1].strip()
        print data_file
        print data_line
        print data_name
        print data_source
        print data_loc
        print key_data
        print func_name
        a = data_var(data_file, data_line, data_name,
                     data_source, data_loc, key_data, func_name)
        data_elem.append(a)
    return data_elem


def get_pointer_table(src_path):
    pointer_workbook = xlrd.open_workbook("data/" + src_path + "/pointer.xls")
    pointer_sheet = pointer_workbook.sheet_by_name("pointer")
    pointer_row = pointer_sheet.nrows
    pointer_elem = []
    for row in range(1, pointer_row):
        pointer_file = ""
        pointer_line = ""
        pointer_name = ""
        pointer_safety = ""
        unsafe_line = ""
        unsafe_reason = ""
        key_data = ""
        func_name = ""
        pointer_file = pointer_sheet.cell_value(
            row, 0).split('/')[-1].split(':')[0]
        pointer_line = pointer_sheet.cell_value(row, 0).split(':')[-1]
        pointer_name = pointer_sheet.cell_value(row, 1).split('@')[0]
        pointer_safety = pointer_sheet.cell_value(row, 2)
        unsafe_line = pointer_sheet.cell_value(row, 5)
        unsafe_reason = pointer_sheet.cell_value(row, 4)
        key_data = pointer_sheet.cell_value(row, 9)
        func_name = pointer_sheet.cell_value(row, 1).split('@')[-1].strip()
        print pointer_file
        print pointer_line
        print pointer_name
        print pointer_safety
        print unsafe_line
        print unsafe_reason
        print key_data
        print func_name
        a = pointer_var(pointer_file, pointer_line, pointer_name,
                        pointer_safety, unsafe_line, unsafe_reason, key_data, func_name)
        pointer_elem.append(a)
    return pointer_elem


def get_space_table(src_path):
    space_workbook = xlrd.open_workbook('data/' + src_path + '/space.xls')
    space_sheet = space_workbook.sheet_by_name('space')
    space_row = space_sheet.nrows
    space_elem = []
    for row in range(1, space_row):
        space_file = ""
        space_line = ""
        space_size = ""
        func_name = ""
        space_file = space_sheet.cell_value(
            row, 0).split('/')[-1].split(':')[0]
        space_line = space_sheet.cell_value(row, 0).split(':')[-1]
        space_size = space_sheet.cell_value(row, 5)
        func_name = space_sheet.cell_value(row, 1)
        print space_file
        print space_line
        print space_size
        print func_name
        a = space(space_file, space_line, space_size, func_name)
        space_elem.append(a)
    return space_elem

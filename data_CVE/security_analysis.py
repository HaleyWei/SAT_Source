# coding=utf-8
import sys
import xlrd
import xlwt
import os
import shutil
import numpy as np
# 工程路径，目前的分析程序是：Juliet-test
# path1:  初始的工程； path2：得到各种数据表之后的工程
path1 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE122_Heap_Based_Buffer_Overflow/s11"
path2 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE415_Double_Free/s02"
path3 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE416_Use_After_Free"
path4 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE415_Double_Free/s01"
path5 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE416_Use_After_Free"
path6 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE121_Stack_Based_Buffer_Overflow/s09"
path7 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE124_Buffer_Underwrite/s04"
path8 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE126_Buffer_Overread/s03"
path9 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE127_Buffer_Underread/s04"
path10 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE401_Memory_Leak/s03"
path11 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE457_Use_of_Uninitialized_Variable/s02"
path12 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE476_NULL_Pointer_Dereference"
path13 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE680_Integer_Overflow_to_Buffer_Overflow"
path14 = "/home/weihaolai/ICKD_analysis/CWE/Desktop/CWE690_NULL_Deref_From_Return/s02"
path15 = "/home/wei/CWE/Desktop/openssl-1.0.1"
path16 = "/home/wei/CWE/Desktop/spec2000/benchmark/164_gzip/src"
path17 = "/home/wei/CWE/Desktop/spec2000/benchmark/175_vpr/src"
path18 = "/home/wei/CWE/Desktop/spec2000/benchmark/179_art/src"
path19 = "/home/wei/CWE/Desktop/spec2000/benchmark/181_mcf/src"
path20 = "/home/wei/CWE/Desktop/spec2000/benchmark/183_equake/src"
path21 = "/home/wei/CWE/Desktop/spec2000/benchmark/186_crafty/src"
path22 = "/home/wei/CWE/Desktop/spec2000/benchmark/188_ammp/src"
path23 = "/home/wei/CWE/Desktop/spec2000/benchmark/197_parser/src"
path24 = "/home/wei/CWE/Desktop/spec2000/benchmark/256_bzip2/src"
path25 = "/home/wei/CWE/Desktop/spec2000/benchmark/300_twolf/src"
path26 = "/home/wei/CWE/Desktop/spec2006"
##############################################-------数据定义--------#########################################################
cfile_num = 0
cfilesize = 0
xtype = "xls"
name = []  # 获得工程中所有文件名，len(name)表示文件个数
typedata = []
file_path = []

unsafe_ptr_num = 0  # 非安全指针数量
op_num = 0  # 所有操作数量
func_call_num = 0
all_var_num = 0  # 指针变量+数据变量
key_var_num = 0  # 指针变量+关键数据变量

####非安全操作需要统计的数据##########
unsafe_op_num = 0  # 非安全操作数量
# 控制关键变量的非安全操作数量，如果一个非安全操作的参数是关键变量，我们就认为此非安全操作控制了关键变量
unsafe_op_control_key_var_num = 0
# 非安全原因：
# 对指针赋值 （赋值:是输入数据：output_to_ptr
# 赋值是非安全指针：unsafe_ptr_to_ptr
# 赋值是包含数值或计算值（将算术或按位运算符应用于一个或多个操作数的结果的值）num_to_ptr
# 赋值的数据存储在栈上：stack_to_ptr
# 指针加偏移 （偏移是输入数据：offset_is_output
# 偏移是变量 ：offset_is_var
# 非安全指针的操作（一个指针确定为非安全指针之后的所有操作）unsafeptr_op
output_to_ptr_num = 0
unsafe_ptr_to_ptr_num = 0
num_to_ptr_num = 0
stack_to_ptr_num = 0
offset_is_output_num = 0
offset_is_var_num = 0
unsafeptr_op_num = 0


#### 输入数据需要统计的相关数量########
output_data_num = 0  # 外部输入数据
output_data_control_key_var_num = 0  # 外部输入控制关键变量（指针+数据）
output_data_control_unsafe_op_num = 0  # 输入控制非安全操作数量
output_data_control_ptr_num = 0  # 输入控制指针数量

#### 指针需要统计的相关数量###############
ptr_num = 0  # 所有指针数量
code_ptr_num = 0  # 代码指针数量
data_ptr_num = 0  # 数据指针数量


###关键变量需要统计的相关数据数量#############
key_data_num = 0  # 数据表中，非指针变量
var_num = 0  # 所有数据数量（非指针变量）

####漏洞检测相关的数据统计########
fn_num = 0
fp_num = 0
findbug_num = 0
badfunc_num = 0

#######################################------------文件读取------------###################################################################
# 统计初始工程中文件个数，以及c/cpp文件个数以及大小


def count_file_type(path):
    global cfile_num, cfilesize
    for file in os.walk(path):
        for each_list in file[2]:
            file_path = file[0] + "/" + each_list
      # os.walk()函数返回三个参数：路径，子文件夹，路径下的文件，利用字符串拼接file[0]和file[2]得到文件的路径
        name.insert(0, file_path)
    print '工程中文件个数', len(name)

    for cfile in name:
        if cfile.split('.')[-1] == 'c' or cfile.split('.')[-1] == 'cpp':
            cfile_num += 1
            #cfilepath=os.path.join(file_path, cfile)
            cfilesize += os.path.getsize(cfile)
    print '工程中含有的c文件个数', cfile_num
    print '工程中c文件的大小', cfilesize


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


###############################----------工程中c\c++文件中常用的数据的数量统计---------------########################################
# 函数 def read_xls完成数据的数量统计工作
# 以文件为粒度进行收集
# 得到整个工程的非安全操作，非安全指针， 操作，指针，变量等数量，
# 为之后的量化指标提供数据支持
# 已有的数据支持是： 已得到juliet-test测试集中c和c++程序的各种数据表。
# count_unsafe_op():  count_unsafe_ptr(): count_op(): count_ptr(): count_var():
def read_xls(path, xtype):
    # ++++++在函数中使用全局变量需要声明 1
    global unsafe_ptr_num, op_num, unsafe_op_num, unsafe_op_control_key_var_num, output_to_ptr_num, unsafe_ptr_to_ptr_num, num_to_ptr_num, stack_to_ptr_num, offset_is_output_num, offset_is_var_num, unsafeptr_op_num, output_data_num, output_data_control_key_var_num, output_data_control_unsafe_op_num, output_data_control_ptr_num, ptr_num, code_ptr_num, data_ptr_num, key_data_num, var_num, fn_num, fp_num, badfunc_num, findbug_num, func_call_num
    # 遍历路径文件夹
    loubao_xls = []
    wubao_xls = []
    all_xls = []
    for file in os.walk(path):
        for each_list in file[2]:
            file_path = file[0] + "/" + each_list
            # os.walk()函数返回三个参数：路径，子文件夹，路径下的文件，利用字符串拼接file[0]和file[2]得到文件的路径
            name.insert(0, file_path)
        all_xls = collect_xls(name, xtype)

    # 每个xls中包含11个sheet表，
    for evey_name in all_xls:
	
        xls_data = xlrd.open_workbook(evey_name)
        table1 = xls_data.sheet_by_name('pointer')
        table2 = xls_data.sheet_by_name('data')
        table3 = xls_data.sheet_by_name('define')
        table4 = xls_data.sheet_by_name('op')
        table5 = xls_data.sheet_by_name('func')
        table6 = xls_data.sheet_by_name('def_use')
        table7 = xls_data.sheet_by_name('unsafe_pointer')
        table8 = xls_data.sheet_by_name('unsafe_op')
        table9 = xls_data.sheet_by_name('space')
        table10 = xls_data.sheet_by_name('cond')
        table11 = xls_data.sheet_by_name('func_call')

        output_data_list = []  # 用于记录每个文件输入数据
        unsafe_op_line_list = []  # 用于记录每个文件的非安全操作所在行号。
	#+++++++++20200822-nxf 输入数据能控制关键数据的操作+非安全操作
        final_unsafe_op_list1= []
	#+++++++++++++++++++20200821-nxf 最终非安全操作行号统计
        final_unsafe_op_list= []
	#++++++20200824-nxf 非安全操作表中信息+将函数调用返回值视为输入数据的操作
        final_unsafe_op_list_0824 =[]
	# ++++++提取表格中的数据我都换了一种方式，因为需要从表第二行开始遍历，get_rows()生成的是迭代器，没找到从第二行开始遍历的方法。使用遍历总行数table.nrows，再用table.cell_value(row, col)提取数据。2
        for row in range(1, table4.nrows):
            op_num += 1

#####+++++20200824-nxf-----
####统计函数调用表中的非安全操作，因为发现现有的非安全操作表中的信息不精确
        for row_11 in range(1,table11.nrows):
	    func_call_num += 1
            line_column = table11.cell_value(row_11, 0)
            func_name_column =table11.cell_value(row_11, 2)
            call_type_column =table11.cell_value(row_11, 3)
            source_column = table11.cell_value(row_11, 9)
            s_bad = str(func_name_column)[-3:]
            #if (s_bad == 'bad' and call_type_column =='lib_call' and source_column =='output'):
	    # -----20200830-nxf-不限制是库函数，看是否能解决那个问题
            if (s_bad == 'bad' and source_column =='output'):
                final_unsafe_op_list_0824.append(line_column)

#####非安全操作相关的量化指标需要的数据统计###################
	# ++++++每个for循环的循环参数按遍历表的序号来定的，防止同名参数混乱 3
        for row_8 in range(1, table8.nrows):

            # 非安全操作数量：
            unsafe_op_num += 1
            flag = 0
# 非安全操作控制关键变量的数量：
            # 关键变量存在于指针表和数据表中
            line_column = table8.cell_value(row_8, 0)  # 获取行号
            unsafe_op_line_list.append(line_column)
	    # ++++++++20200824-nxf
            final_unsafe_op_list_0824.append(line_column)
            #+++++++++20200822-nxf
            final_unsafe_op_list1.append(line_column)

            for row_4 in range(1, table4.nrows):
                line1_column = table4.cell_value(row_4, 0)
                src_column = table4.cell_value(row_4, 3)
                dst_column = table4.cell_value(row_4, 4)
		# ++++++将isinstance改成‘==’比较字符串 4
                if line_column == line1_column:
                    for row_1 in range(1, table1.nrows):
                        name_column = table1.cell_value(row_1, 1)
                        key_data_column = table1.cell_value(row_1, 9)
			# ++++++src_column和dst_column可能有多个数据，表格中我用空格隔开了，后面有split(' ')的都是这个原因 5   
                        if name_column in src_column.split(' '):
                            if (key_data_column == 'key_control_data' or key_data_column == 'key_non_control_data') and flag == 0:
                                # unsafe_op_control_key_var_num += 1
				# ++++++++20200821-nxf
                                final_unsafe_op_list.append(line1_column)
                                flag = 1
                        if name_column in dst_column.split(' '):
                            if (key_data_column == 'key_control_data' or key_data_column == 'key_non_control_data') and flag == 0:
                                # unsafe_op_control_key_var_num += 1
				# ++++++++20200821-nxf
                                final_unsafe_op_list.append(line1_column)
                                flag = 1

                    for row_2 in range(1, table2.nrows):
                        name_column = table2.cell_value(row_2, 1)
                        key_data_column = table2.cell_value(row_2, 4)
                        if name_column in src_column.split(' '):
                            if (key_data_column == 'key_control_data' or key_data_column == 'key_non_control_data') and flag == 0:
                                unsafe_op_control_key_var_num += 1
				# ++++++++20200821-nxf
                                final_unsafe_op_list.append(line1_column)
                                flag = 1
                        if name_column in dst_column.split(' ') :
                            if (key_data_column == 'key_control_data' or key_data_column == 'key_non_control_data') and flag == 0:
                                unsafe_op_control_key_var_num += 1
				# ++++++++20200821-nxf
                                final_unsafe_op_list.append(line1_column)
                                flag = 1
# 非安全原因数量：
            unsafe_reason_column = table8.cell_value(row_8, 5)
	    # ++++++原因5
	    for unsafe_reason in unsafe_reason_column.split(' '):
                if unsafe_reason == 'output_to_ptr':
                    output_to_ptr_num += 1
                if unsafe_reason == 'unsafe_ptr_to_ptr':
                    unsafe_ptr_to_ptr_num += 1
                if unsafe_reason == 'num_to_ptr':
                    num_to_ptr_num += 1
                if unsafe_reason == 'stack_to_ptr':
                    stack_to_ptr_num += 1
                if unsafe_reason == 'offset_is_output':
                    offset_is_output_num += 1
                if unsafe_reason == 'offset_is_var':
                    offset_is_var_num += 1
                if unsafe_reason == 'unsafe_ptr_op':
                    unsafeptr_op_num += 1

#####输入数据相关的量化指标需要的数据统计###################
# 获取每个文件的输入数据
        for row_2 in range(1, table2.nrows):
            var_num += 1
            source_data_column = table2.cell_value(row_2, 6)
            name_column = table2.cell_value(row_2, 1)
	    # ++++++20200821-nxf
            line_column =table2.cell_value(row_2, 0)

            if source_data_column == 'output':
                output_data_num += 1
                output_data_list.append(name_column)

# 输入数据控制关键变量
# 算法：
# def-use表中，
# 最简单情况：src_arg是输入数据， dst_arg是关键变量，记录
# src_arg是关键变量（指针 or 数据）, 追溯来源，看是否有输入数据（根据def-use中的内容追溯）

# def-use相关：
        for row_6 in range(1, table6.nrows):
            line_column = table6.cell_value(row_6, 0)
            src_arg_column = table6.cell_value(row_6, 2)
            dst_arg_column = table6.cell_value(row_6, 3)
            src_column = table6.cell_value(row_6, 4)
            dst_column = table6.cell_value(row_6, 5)
            src_list = list(set(src_column.split(' ')))
            dst_list = list(set(dst_column.split(' ')))

        # 输入数据控制关键数据变量
            for row_2 in range(1, table2.nrows):
                name_column = table2.cell_value(row_2, 1)
                key_data_column = table2.cell_value(row_2, 4)
                # src_arg是输入数据， dst_arg是关键变量
                if name_column in dst_arg_column.split(' '):
                    if key_data_column is not 'normal':
			for arg_src in src_arg_column.split(' '): 
                            if arg_src in output_data_list:
                                output_data_control_key_var_num += 1
				# ++++++++20200821-nxf
                                final_unsafe_op_list.append(line_column)
				final_unsafe_op_list1.append(line_column)

                # src_arg是关键变量
                if name_column in src_arg_column.split(' '):
                    if key_data_column is not 'normal':
                            # 关键变量的来源是输入数据，即输入数据控制了关键变量
                        for sl in src_list:
                            for row_4 in range(1, table4.nrows):
                                line_column4 = table4.cell_value(row_4, 0)
                                src_column4 = table4.cell_value(row_4, 3)
                                if sl == line_column4:
				    for s_c in src_column4.split(' '): 
                                        if s_c in output_data_list:
                                            #output_data_control_key_var_num += 1
					    # ++++++++20200821-nxf
                                            final_unsafe_op_list.append(line_column)
					    final_unsafe_op_list1.append(line_column)
	    # ++++++数据我按照变量来处理的，也包括指针，是否应该把这两种区分一下 6

            # 输入数据控制关键指针变量
            for row_1 in range(1, table1.nrows):
                name_column = table1.cell_value(row_1, 1)
                key_data_column = table1.cell_value(row_1, 9)
                # src_arg是输入数据， dst_arg是关键变量
                if name_column in dst_arg_column.split(' '):
                    if key_data_column is not 'normal':
			for arg_src in src_arg_column.split(' '):
                            if arg_src in output_data_list:
                                #output_data_control_key_var_num += 1
				# ++++++++20200821-nxf
                                final_unsafe_op_list.append(line_column)
				final_unsafe_op_list1.append(line_column)

                # src_arg是关键变量
                if name_column in src_arg_column.split(' '):
                    if key_data_column is not 'normal':
                            # 关键变量的来源是输入数据，即输入数据控制了关键变量
                        for sl in src_list:
                            for row_4 in range(1, table4.nrows):
                                line_column4 = table4.cell_value(row_4, 0)
                                src_column4 = table4.cell_value(row_4, 3)
                                if sl == line_column4:
			            for s_c in src_column4.split(' '):
                                       if s_c in output_data_list:
                                            #output_data_control_key_var_num += 1
					    # ++++++++20200821-nxf
                                	    final_unsafe_op_list.append(line_column)
					    final_unsafe_op_list1.append(line_column)
					    # ++++++20200830-nxf
                                	    final_unsafe_op_list_0824.append(line_column)

# 输入数据控制非安全操作
# 算法：
# def_use表中，
# 找到非安全操作，根据行号判断
# 如果是，先对参数进行判断是否是输入数据
# 之后，根据def-use表，追溯来源，寻找输入数据
	    # ++++++因为每行的操作只有一条，考虑遍历一行可能有多个符合情况，用flag标识代替 7
            for row_8 in range(1, table8.nrows):
		flag = 0
                unsafe_op_line_column = table8.cell_value(row_8, 0)
                if line_column == unsafe_op_line_column:
		    for s_a in src_arg_column.split(' '):
                    	if s_a in output_data_list:
                            flag = 1
    
                        else:
                            for sl in src_list:
                                for row_4 in range(1, table4.nrows):
                                    line_column4 = table4.cell_value(row_4, 0)
                                    src_column4 = table4.cell_value(row_4, 3)
                                    if sl == line_column4:
					for s_c in src_column4.split(' '):
                                            if s_c in output_data_list:
                                                flag = 1
		if flag == 1:
		    output_data_control_unsafe_op_num += 1


# 输入数据控制指针
# 算法：
# def-use 表中：
# 最简单情况：src_arg是输入数据， dst_arg是指针，记录
# src_arg是指针, 追溯来源，看是否有输入数据（根据def-use中的内容追溯）
	    # ++++++原因7
            for row_1 in range(1, table1.nrows):
                flag = 0
                name_column = table1.cell_value(row_1, 1)
                # src_arg是输入数据， dst_arg是指针
                if name_column in dst_arg_column.split(' '):
		    for s_c in src_arg_column.split(' '):
                        if s_c in output_data_list:
                            flag = 1

                # src_arg是指针，指针的来源是输入数据，即输入数据控制了指针
                if name_column in src_arg_column.split(' '):
                    for sl in src_list:
                        for row_4 in range(1, table4.nrows):
                            line_column4 = table4.cell_value(row_4, 0)
                            src_column4 = table4.cell_value(row_4, 3)
                            if sl == line_column4:
				for s_c in src_column4.split(' '):
                                    if s_c in output_data_list:
                                        flag = 1
		if flag == 1:
		    output_data_control_ptr_num += 1


#####指针相关的量化指标需要的数据统计###################
        for row_1 in range(1, table1.nrows):
            ptr_num += 1
        for row_7 in range(1, table7.nrows):
            unsafe_ptr_num += 1

#####关键变量相关的量化指标需要的数据统计###################
        for row_2 in range(1, table2.nrows):
            key_data_column = table2.cell_value(row_2, 4)
            if key_data_column == 'key_non_control_data' or key_data_column == 'key_control_data':
                key_data_num += 1

#######bad函数作用域，以及漏洞检测相关数据统计########
        # 检测算法:
        # 如果非安全操作表为空,则漏报.(因为每个文件中都有bad函数,则必定存在一个漏洞)
        # 如果非安全操作表不为空,则进行如下检测:
        # 如果行号在对应的bad函数的作用域中,则正确找到
        # 如果行号没在bad函数作用域中,则误报
        # 统计good函数行号
        good_line = {}
        search_line = []
        for row_5 in range(1, table5.nrows):
            func_name_column = table5.cell_value(row_5, 0)
            start_line_column = table5.cell_value(row_5, 3)
            finish_line_column = table5.cell_value(row_5, 4)
            if 'good' in str(func_name_column):
                for i in range(int(start_line_column), int(finish_line_column) + 1):
                    # good_line.append(str(i))
                    good_line[str(i)] = start_line_column
        for row_5 in range(1, table5.nrows):
            func_name_column = table5.cell_value(row_5, 0)
            start_line_column = table5.cell_value(row_5, 3)
            finish_line_column = table5.cell_value(row_5, 4)
	    # ++++20200821-nxf将final_unsafe_op_list中相同的元素删除是否会对fp， fn有影响？
            final_unsafe_op_list1 = np.unique(final_unsafe_op_list)

            #++++++++20200821-nxf
            # 解决bad函数统计问题
            str_bad = str(func_name_column)[-3:]
            str_good = '0'
            if 'good' in func_name_column:
                str_good = '1'
            if str_bad == 'bad':
                badfunc_num += 1
                # 非安全操作不为空，遍历非安全操作表
		#+++++++20200821-nxf将unsafe_op_line_list替换为final_unsafe_op_list，目的是看看漏报误报会不会少
		#+++++++20200822-nxf unsafe_op_list是非安全操作
                #+++++++20200822-nxf final_unsafe_op_list1 是输入控制关键数据的操作+非安全操作 
                #+++++++20200822-nxf final_unsafe_op_list是输入控制关键数据的操作+能控制关键数据的非安全操作   
                #+++++++20200822-nxf 理论上 final_unsafe_op_list1 就能使fn=0  
                #+++++++20200822-nxf 通过修改三者观察fn，fp     

                # +++++++20200824-nxf 将final_unsafe_op_list_0824 观察fn， fp
                if final_unsafe_op_list_0824:
                    find_flag = 0
                    for line in final_unsafe_op_list_0824:
                        if int(line) >= int(start_line_column) and int(line) <= int(finish_line_column):
                            find_flag = 1  # 找到了漏洞
                        elif line in good_line and good_line[line] not in search_line:
                            fp_num += 1  # 认为是误报
                            search_line.append(good_line[line])
			    wubao_xls.append(evey_name)
			    

                    if find_flag == 1:
                        findbug_num += 1
                    if find_flag == 0:
                        fn_num += 1  # 在bad函数中没有找到漏洞，则发生漏报
			loubao_xls.append(evey_name)

                # 非安全操作为空也是一种漏报，这个和非安全操作的精确度有关
                if not final_unsafe_op_list_0824:
                    fn_num += 1
		    loubao_xls.append(evey_name)
    loubao_xls = list(set(loubao_xls))
''' 
    for loubao in loubao_xls:
	oldfile_c = loubao.split('.')[0] + '.c'
	oldfile_cpp = loubao.split('.')[0] + '.cpp'
	newfile_xls = "/home/weihaolai/loubao/" + loubao.split('/')[-1]
	shutil.copyfile(loubao, newfile_xls)
	if os.path.exists(oldfile_c):
	    newfile_c = "/home/weihaolai/loubao/" + oldfile_c.split('/')[-1]  
	    shutil.copyfile(oldfile_c, newfile_c)
        elif os.path.exists(oldfile_cpp):
	    newfile_cpp = "/home/weihaolai/loubao/" + oldfile_cpp.split('/')[-1]
            shutil.copyfile(oldfile_cpp, newfile_cpp)
	print loubao 
    for wubao in wubao_xls:
	print wubao
'''

##################################------------量化指标（由粗到细）----------------################################################
# 从工程角度， C\C++文件占比越大，安全性风险越大，或者说c\c++越大(总代码量越大)，安全性风险越大（最粗粒度）
            # 因为软件中，不会只有c，c++文件，还有其他文件类型，因此我们需要对各种文件类型数量进行统计。
            # 看c文件，c++文件占比。
            # c/c++文件占比越大，我们之后分析的任务越大，可能存在的安全风险越高。
# 从C\c++程序角度，从非安全操作， 输入数据， 指针，关键变量四个方面制定一些软件安全性的量化指标
# 目前制定了14条量化指标

# 工程角度：----------------------------
# c、c++程序相关的量化指标
def cfile_Quantitative_indicators():
            # 指标：
            # 00. c程序的数量越多，大小越大，安全性风险越高
    print '工程中文件个数', len(name)
    print '工程中含有的c文件个数', cfile_num
    print '工程中c文件的大小', cfilesize


# c\c++文件角度：---------------------------------------------------------------------------------
# 非安全操作相关的量化指标
def unsafe_op_Quantitative_indicators():
        #  指标：
        #  01.非安全操作占所有操作的比例 q1
        #  02.非安全操作原因：各种原因的数量统计   q2_1 ~ q2_7
        #  03.非安全操作控制关键变量的比例，如果一个非安全操作的参数是关键变量，我们就认为此非安全操作控制了关键变量。q3
    # q1 = unsafe_op_num / op_num
    if op_num:
    	q1 = float(unsafe_op_num) / op_num
	q3 = float(unsafe_op_control_key_var_num) / unsafe_op_num
    else:
	q1 = 0
	q3 = 0
    q2_1 = output_to_ptr_num
    q2_2 = unsafe_ptr_to_ptr_num
    q2_3 = num_to_ptr_num
    q2_4 = stack_to_ptr_num
    q2_5 = offset_is_output_num
    q2_6 = offset_is_var_num
    q2_7 = unsafeptr_op_num
    # q3 = unsafe_op_control_key_var_num / unsafe_op_num
    
    q3_1=unsafe_op_control_key_var_num

    # print('非安全操作占所有操作的比例', q1) 
    # print('非安全操作控制关键变量的比例',q3) 
    # print('非安全操作原因,各种原因的数量统计：\n\t')
    # print('对指针赋值',q2_1)
    # print('赋值是非安全指针',q2_2)
    # print(' 赋值是包含数值或计算值',q2_3)
    # print('赋值的数据存储在栈上',q2_4)
    # print('指针加偏移 ',q2_5)
    # print('偏移是变量 ',q2_6)
    # print('非安全指针的操作',q2_7) 
    print '函数调用返回语句数量', func_call_num
    print '赋值语句数量', op_num
    print '非安全操作数量', unsafe_op_num
    print '非安全操作占所有操作的比例', q1
    print '非安全操作控制关键变量的比例', q3
    print '非安全操作控制关键变量的数量',q3_1
    print '非安全操作原因,各种原因的数量统计：\n\t'
    print '对指针赋值', q2_1
    print '赋值是非安全指针', q2_2
    print '赋值是包含数值或计算值', q2_3
    print '赋值的数据存储在栈上', q2_4
    print '指针加偏移 ', q2_5
    print '偏移是变量 ', q2_6
    print '非安全指针的操作', q2_7, '\n\t'


# 输入数据相关的量化指标
def input_Quantitative_indicators():
    #  指标：
    #  04.输入数据占所有数据比例
    #  05.输入数据控制关键变量的比例，如何体现控制？（关键变量从指针表和数据表中得到）
    #  06.输入数据控制非安全操作的比例，如何体现控制？
    #  07.输入数据对指针的影响和控制， 如何体现控制？
    # 05.06.07需要考虑def——use表得到传递关系。。。
    # 比例越大，可能存在的安全风险越大
    # q4 = output_data_num / var_num
    # q5 = output_data_control_key_var_num / output_data_num
    # q6 = output_data_control_unsafe_op_num / output_data_num
    # q7 = output_data_control_ptr_num / output_data_num
    q4 = float(output_data_num) / var_num
    if output_data_num != 0:
    	q5 = float(output_data_control_key_var_num) / output_data_num
	q6 = float(output_data_control_unsafe_op_num) / output_data_num
	q7 = float(output_data_control_ptr_num) / output_data_num
    else:
	q5 = 0
	q6 = 0
	q7 = 0
    q5_1 = output_data_control_key_var_num
    
    
    # print('输入数据占所有数据比例', q4) 
    # print('输入数据控制关键变量的比例', q5)
    # print('输入数据控制非安全操作的比例',q6) 
    # print('输入数据控制指针的比例',q7)
    print '所有数据的数量', var_num
    print '输入数据的数量', output_data_num
    print '输入数据占所有数据比例', q4
    print '输入数据控制关键变量的比例', q5
    print '输入数据控制关键变量的数量', q5_1
    print '输入数据控制非安全操作的比例', q6
    print '输入数据控制指针的比例', q7, '\n\t'


# 指针相关的量化指标
def ptr_Quantitative_indicators():
    # 指标：
    # 08.指针占所有变量的比例，指针操作越多，可能存在的安全风险越大
    # 09.代码指针占所有指针的比例，因代码指针更容易被利用，因此比例越高，安全性风险越大
    # 10.数据指针占所有指针的比例，数据指针的利用比较难，因此比例越高，安全性越高
    # 11.非安全指针占所有指针的比例，比例越高，安全性风险越大
    # 09.10可能不太容易区分，暂时不做量化

    # q8 = ptr_num / (ptr_num + var_num)
    # q9=
    # q10=
    # q11 = unsafe_ptr_num / ptr_num
    #q8 = float(ptr_num) / (ptr_num + var_num)
    if var_num != 0:
        q8 = float(ptr_num) / var_num
    else:
        q8 = 0
    if ptr_num != 0:
        q11 = float(unsafe_ptr_num) / ptr_num
    else:
        q11 = 0

    # print('指针占所有变量的比例', q8) 
    # print('代码指针占所有指针的比例', )
    # print('数据指针占所有指针的比例',) 
    # print('非安全指针占所有指针的比例',q11)
    print '非安全指针数量', unsafe_ptr_num
    print '指针变量数量', ptr_num
    print '指针占所有变量的比例', q8
    print '代码指针占所有指针的比例', 
    print '数据指针占所有指针的比例',
    print '非安全指针占所有指针的比例', q11, '\n\t'

# 关键变量相关的量化指标：关键变量包括指针和数据


def key_var_Quantitative_indicators():
    global key_var_num
    # 指标
    # 12.关键变量占所有变量的比例，比例越高，安全性风险越高
    # 13.各种关键变量占总关键变量的比例，按照数据需求中应该是：控制数据占比和非控制数据占比，但是代码指针和数据指针目前不进行区分
    # 因此关键变量分为指针占比和数据占比
    #all_var_num = ptr_num + var_num
    all_var_num = var_num
    #key_var_num = ptr_num + key_data_num
    key_var_num = key_data_num
    #p12 = key_var_num / all_var_num
    #p13_1 = ptr_num / key_var_num
    #p13_2 = key_data_num / key_var_num
    p12 = float(key_var_num) / all_var_num
    p13_1 = float(ptr_num) / key_var_num
    p13_2 = float(key_data_num) / key_var_num
    # print('关键变量占所有变量的比例',p12) 
    # print('各种关键变量占总关键变量的比例:\n\t')
    # print('指针变量占总关键变量的比例:', p13_1)
    # print('关键数据变量占总关键变量的比例:', p13_2)
    print '关键变量数量', key_var_num
    print '关键变量占所有变量的比例', p12
    print '各种关键变量占总关键变量的比例:\n\t'
    print '指针变量占总关键变量的比例:', p13_1
    print '关键数据变量占总关键变量的比例:', p13_2, '\n\t'

#####################获取bad函数作用域并统计bad函数个数,并实施检测并统计结果###################


def find_bug_Quantitative_indicators():
    # 指标
    # 14.漏报
    # 15.误报
    # 16.bad函数个数，只对juliet-test适用
    # 17.找到漏洞个数
    p14 = fn_num
    p15 = fp_num
    p16 = badfunc_num
    p17 = findbug_num
    # print('漏报',p14) 
    # print('误报:',p15)
    # print('bad函数个数:', p16)
    # print('找到漏洞个数:', p17)
    print '漏报', p14
    print '误报:', p15
    print 'bad函数个数:', p16
    print '找到漏洞个数:', p17


#############程序入口#################################
if __name__ == '__main__':
    src_path = sys.argv[1]
    path= "/home/weihaolai/ICKD_analysis/data_CVE/" + src_path + "/code"
    read_xls(path, xtype)
    print('量化指标：')
    # c、c++程序相关的量化指标
    # cfile_Quantitative_indicators(path1)
    # count_file_type(path14)
# 非安全操作相关的量化指标
    unsafe_op_Quantitative_indicators()
# 指针相关的量化指标
    ptr_Quantitative_indicators()
# 输入数据相关的量化指标
    input_Quantitative_indicators()
# 关键变量相关的量化指标：关键变量包括指针和数据
    key_var_Quantitative_indicators()
# 获取bad函数作用域并统计bad函数个数
    find_bug_Quantitative_indicators()

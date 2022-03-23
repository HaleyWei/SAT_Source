# # coding:utf-8
from joern.all import JoernSteps
from py2neo.packages.httpstream import http
http.socket_timeout = 9999


class rg:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class item:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst


# 获取所有函数节点
def getALLFuncNode(db):
    query_str = "queryNodeIndex('type:Function')"
    results = db.runGremlinQuery(query_str)
    return results


# 获取所有函数的号及名称
def getALLFuncNodeId_Name(db):
    query_str = "queryNodeIndex('type:Function')"
    results = db.runGremlinQuery(query_str)
    func_id = []
    for re in results:
        a = rg(re._id, re.properties['name'])
        func_id.append(a)

    return func_id


# 获取函数路径
def getFuncFile(db, func_id):
    query_str = "g.v(%d).in('IS_FILE_OF').filepath" % func_id
    ret = db.runGremlinQuery(query_str)

    return ret[0]


# 获取节点的def
def get_def_node(db, cfg_node_id):
    query_str = "g.v(%d).out('DEF')" % cfg_node_id
    results = db.runGremlinQuery(query_str)
    return results


# 获取函数的CFG节点
def getCFGNodes(db, func_id):
    query_str = 'queryNodeIndex("functionId:%s AND isCFGNode:True")' % func_id
    cfgNodes = db.runGremlinQuery(query_str)

    return cfgNodes


# 获取函数所有变量
def get_fun_var(db, funcId):
    query_iddecl_str = 'queryNodeIndex("functionId:%d AND type:IdentifierDeclStatement")' % funcId
    results = db.runGremlinQuery(query_iddecl_str)
    var = []
    if results != []:
        for re in results:
            def_node = get_def_node(db, re._id)
            for db_node in def_node:
                var.append(str(db_node.properties['code']))
    query_iddecl_pra = 'queryNodeIndex("functionId:%d AND type:Parameter")' % funcId
    results_2 = db.runGremlinQuery(query_iddecl_pra)
    if results_2 != []:
        for re_2 in results_2:
            def_node = get_def_node(db, re_2._id)
            for db_node in def_node:
                var.append(str(db_node.properties['code']))
    return var


# 获取下一个节点
def getNextNode(db, node_id):
    query_str = "g.v(%d).out('IS_AST_PARENT')" % node_id
    ret = db.runGremlinQuery(query_str)
    return ret


# 获取语句类型，如果是表达式，则输出下一个节点的类型，否则输出当前类型
def get_type(db, node):
    if node.properties['type'] == "ExpressionStatement":
        result = getNextNode(db, node._id)
        for ret in result:
            return ret.properties['type']
    else:
        return node.properties['type']


# 获取节点的use
def get_use_node(db, cfg_node_id):
    query_str = "g.v(%d).out('USE')" % cfg_node_id
    results = db.runGremlinQuery(query_str)
    return results


# 获取当前节点属于CFG节点的父节点
def getLastNode(db, node_id):
    query_str = "g.v(%d).in('IS_AST_PARENT')" % node_id
    ret = db.runGremlinQuery(query_str)
    if ret:
        if ret[0].properties['isCFGNode'] == 'True':
            return ret[0]
        else:
            return getLastNode(db, ret[0]._id)
    else:
        return "null"


def getCFGEdges(db, func_id):
    query_str = """queryNodeIndex('functionId:%s AND isCFGNode:True').outE('FLOWS_TO')""" % (
        func_id)
    cfgEdges = db.runGremlinQuery(query_str)
    return cfgEdges


def getDDGEdges(db, func_id):
    query_str = """queryNodeIndex('functionId:%s AND isCFGNode:True').outE('REACHES')""" % (
        func_id)
    ddgEdges = db.runGremlinQuery(query_str)
    return ddgEdges


def getLocation(node):
    count = 0
    if 'location' in str(node):
        location = node.properties['location'].split(':')[0]
        count = int(location)
    return count


def statement_Type(node_type):
    str_type = ""
    if node_type == "IdentifierDeclStatement" or node_type == "Parameter" or node_type == "ArrayIndexing":
        str_type = "define"
    elif node_type == "ForInit" or node_type == "IncDecOp" or node_type == "AssignmentExpr" or node_type == "UnaryOp":
        str_type = "op"
    elif node_type == "ContinueStatement" or node_type == "Condition" or node_type == "GotoStatement" or node_type == "BreakStatement" or node_type == "Label":
        str_type = "cond"
    elif node_type == "CallExpression":
        str_type = "call"
    elif node_type == "ReturnStatement":
        str_type = "ret"
    elif node_type == "Statement" or node_type == "Identifier":
        str_type = "unknow"
    return str_type


def get_call_var(db, func_id):
    call_list = []
    query_iddecl_str = 'queryNodeIndex("functionId:%d AND type:Callee")' % func_id
    results = db.runGremlinQuery(query_iddecl_str)
    if results:
        for re in results:
            call_list.append(re.properties['code'])
    return call_list


def getData_type(db, node_id, number):
    query_str = "g.v(%d).out('IS_AST_PARENT')" % node_id
    ret = db.runGremlinQuery(query_str)
    if ret and len(ret) > number:
        idf = ""
        ndf = ""
        for r in ret:
            if r.properties['childNum'] == '0' and (r.properties['type'] == 'IdentifierDeclType' or r.properties['type'] == 'ParameterType'):
                idf = r.properties['code']
            if (r.properties['childNum'] == '1' or r.properties['childNum'] == '0') and r.properties['type'] == 'Identifier':
                ndf = r.properties['code']
        if idf != "" and ndf != "":
            return idf, ndf
        else:
            query_str_2 = "g.v(%d).out('IS_AST_PARENT')" % ret[number]._id
            ret_2 = db.runGremlinQuery(query_str_2)
            if ret_2:
                idf_2 = ""
                ndf_2 = ""
                for r in ret_2:
                    if r.properties['childNum'] == '0' and (r.properties['type'] == 'IdentifierDeclType' or r.properties['type'] == 'ParameterType'):
                        idf_2 = r.properties['code']
                    if (r.properties['childNum'] == '1' or r.properties['childNum'] == '0') and r.properties['type'] == 'Identifier':
                        ndf_2 = r.properties['code']
                if idf_2 != "" and ndf_2 != "":
                    return idf_2, ndf_2
    return "null", "null"


def getStaticNode(db, node_id):
    query_str = "g.v(%d).in('IS_AST_PARENT')" % node_id
    ret = db.runGremlinQuery(query_str)
    query_left = "g.v(%d).out" % ret[0]._id
    ret_left = db.runGremlinQuery(query_left)
    if ret_left[0].properties['code'].strip() == "static":
        return True, ret_left[0].properties['location'].split(':')[0]
    else:
        return False, 0


def getVarUse(db, func_id):
    query_str = 'queryNodeIndex("functionId:%s AND type:Identifier")' % func_id
    result = db.runGremlinQuery(query_str)
    return result


def get_all_data(db, func_id):
    list_data_node = []
    query_iddecl_str = 'queryNodeIndex("functionId:%s AND type:IdentifierDeclStatement")' % func_id
    results = db.runGremlinQuery(query_iddecl_str)
    for re in results:
        if 'location' in str(re):
            list_data_node.append(re)
    query_param_str = 'queryNodeIndex("functionId:%s AND type:Parameter")' % func_id
    results = db.runGremlinQuery(query_param_str)
    for re in results:
        if 'location' in str(re):
            list_data_node.append(re)
    return list_data_node

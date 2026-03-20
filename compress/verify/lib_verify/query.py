from .query_int import *
import sys,os
sys.path.append('../..')
from lib import *

def querydict_(list1:list) -> dict:
    """新建一个小的dict，然后对应到list区间的下标

    Args:
        list1 (list): [description]

    Returns:
        dict: [description]
    """
    dmp = 100000
    dict1 = {}
    min = 0
    flag = math.floor(list1[0]/dmp)
    for j in range(len(list1)):
        if math.floor(list1[j]/dmp) != flag:
            dict1[flag] = [min,j-1]
            flag = math.floor(list1[j]/dmp)
            min = j
        if j == len(list1)-1:
            dict1[flag] = [min,j]
    return dict1

def optimize_querylist(querylist:list,datas_dict:dict):
    #优化querylist
    #获取所有的querylist number，重新构建一个querylist
    querylist_new = []
    for i in range(len(querylist)):
        querylist_new.append(dataInt(querylist[i].number))
    for i in range(len(querylist)-1):
        list_index = list(querylist[i].indexs & querylist[i+1].indexs)
        if len(list_index)==0:
            continue
        list1 = []
        ##注意这个data应该是一个dict，通过key——value查找
        for j in range(len(list_index)):
            list1.append([list_index[j],datas_dict[list_index[j]]])

        list1.sort(key=lambda list1: list1[1].ipEnd - list1[1].ipIndex)

        #新构建的querylist
        querylist_new[i].indexs.add(list1[0][0])
        # querylist_new[i+1].indexs.add(list1[0][0])
    return querylist_new

def get_querylist(datas_dict:dict,file_querylist:str):
    """
    Args:
        file (str): [description]

    Returns:
        list[dataInt]: [description]
    """
    if os.path.exists(file_querylist):
        tmp1 = loadFromDisk(file_querylist)
        querylist = tmp1[0]
        querydict = tmp1[1]
    else:
        set1 = add_number(datas_dict)
        list1 = list(set1)
        list1.sort()
        # querylist_number = list1
        querydict = querydict_(list1)
        querylist = [dataInt(x) for x in list1]
        add_index(datas_dict, querylist, querydict)
        saveToDisk([querylist,querydict], file_querylist)
    return  [querylist,querydict]


def get_optimize_querylist(datas_dict:dict,file_querylist:str):
    """
    Args:
        file (str): [description]

    Returns:
        list[dataInt]: [description]
    """
    if os.path.exists(file_querylist):
        tmp1 = loadFromDisk(file_querylist)
        querylist_new = tmp1[0]
        querydict = tmp1[1]
    else:
        set1 = add_number(datas_dict)
        list1 = list(set1)
        list1.sort()
        querydict = querydict_(list1)
        querylist = [dataInt(x) for x in list1]
        add_index(datas_dict, querylist, querydict)
        querylist_new = optimize_querylist(querylist,datas_dict)
        saveToDisk([querylist_new,querydict], file_querylist)
    return  [querylist_new,querydict]


# def query_int(ips:list, data_file:str,query_file:str) -> list[localda]:
#     """查询ips的经纬度

#     Args:
#         ips ([type]): [description]
#         file (str): [description]

#     Returns:
#         list[localda]: [description]
#     """
#     datas = getDatas(data_file)
#     datas_dict = setdict(datas)  #将数据变成dict
#     query = get_querylist(datas_dict,query_file)
#     querylist = query[0]
#     querydict = query[1]
#     ips = ips if type(
#         ips[0]) == int else [addressToInt(iptmp) for iptmp in ips]

#     return [localda(ip, *query_int_ip(ip,datas_dict,querylist,querydict)) for ip in ips]

def query_int2(ips:list, data_file:str,query_file:str) -> list[localda]:
    """查询ips的经纬度

    Args:
        ips ([type]): [description]
        file (str): [description]

    Returns:
        list[localda]: [description]
    """
    datas = getDatas(data_file)
    datas_dict = setdict(datas)  #将数据变成dict
    query = get_optimize_querylist(datas_dict,query_file)
    querylist = query[0]
    querydict = query[1]
    ips = ips if type(
        ips[0]) == int else [addressToInt(iptmp) for iptmp in ips]

    return [localda(ip, *query_int_ip2(ip,datas_dict,querylist,querydict)) for ip in ips]


def query_(ips:list, datas_dict:dict,querylist:list[dataInt],querydict:dict) -> list[localda]:
    """查询ips的经纬度

    Args:
        ips ([type]): [description]
        file (str): [description]

    Returns:
        list[localda]: [description]
    """
    ips = ips if type(
        ips[0]) == int else [addressToInt(iptmp) for iptmp in ips]

    return [localda(ip, *query_int_ip2(ip,datas_dict,querylist,querydict)) for ip in ips]



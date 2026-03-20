import math,os
from lib.bgp_class import *
from lib.binarySearch import *
from lib.other import *

def checkSearchDatas(datas: list) -> list:
    """返回网段最小的 data 的经纬度.

    Args:
        datas (list[data]): []

    Returns:
        tuple[float, float]: []
    """
    if len(datas) <= 0 or datas == None:
        return [360, 360]

    datas.sort(key=lambda data: data.ipEnd - data.ipIndex)

    return [datas[0].lng, datas[0].lat]
    
def query_index(list1: list[dataInt], start: int, end: int, index):
    """添加dataInt中index的元素

    Args:
        list1 (list[dataInt]): [description]
        start (int): [description]
        end (int): [description]
        index (int): [description]
    """
    for i in range(start, end + 1):
        list1[i].addIndex(index)

def setdict(datas:list[data]) -> dict:
    """将list变成dict

    Args:
        datas_remove (list): [description]

    Returns:
        dict: [description]
    """
    key = []
    for i in range(len(datas)):
       key.append('{}'.format(i))
    datas_remove_dict = dict(zip(key,datas))
    return datas_remove_dict

def add_number(datas_dict:dict) -> set[int]:
    """添加number列表

    Args:
        dbs (list[data]): [description]
    Returns:
        set[int]: [description]
    """
    set1 = set()
    for key,value in datas_dict.items():
        # ipIndex下标
        print(value.iprefix)
        set1.add(value.ipIndex)
        set1.add(value.ipEnd)
    return set1


def add_index(dbs:dict, list1: list[dataInt],querydict:dict):
    """给number列表添加index

    Args:
        dbs (list[data]): [description]
        list1 (list[dataInt]): [description]
    """
    for key,value in dbs.items():
        # ipIndex下标
        print(value.iprefix)
        tmp = 100000
        value_pre = querydict.get(math.floor(value.ipIndex/tmp))
        value_next = querydict.get(math.floor(value.ipEnd/tmp))
        ipIndex_ = binarySearch(list1, value_pre[0], value_pre[1], value.ipIndex)
        # inEnd下标
        ipEnd_ = binarySearch(list1,value_next[0], value_next[1], value.ipEnd)
        # 插入下标
        query_index(list1, ipIndex_, ipEnd_, key) #挂下标
        # tmp.append([ipIndex_tuple, ipEnd_tuple])

# def hash_table(list1:list) -> dict:
#     """新建一个小的dict，然后对应到list区间的下标

#     Args:
#         list1 (list): [description]

#     Returns:
#         dict: [description]
#     """
#     dmp = 100000
#     dict1 = {}
#     min = 0
#     flag = math.floor(list1[0]/dmp)
#     for j in range(len(list1)):
#         if math.floor(list1[j]/dmp) != flag:
#             dict1[flag] = [min,j-1]
#             flag = math.floor(list1[j]/dmp)
#             min = j
#         if j == len(list1)-1:
#             dict1[flag] = [min,j]
#     return dict1

# def get_querylist(datas:dict,file_querylist:str):
#     """得到数据的中间查询数组
#     Args:
#         file (str): [description]

#     Returns:
#         list[dataInt]: [description]
#     """
#     if os.path.exists(file_querylist):
#         tmp1 = loadFromDisk(file_querylist)
#         list1 = tmp1[0]
#         querydict = tmp1[1]
#     else:
#         set1 = add_number(datas)
#         list1 = list(set1)
#         list1.sort()
#         querydict = hash_table(list1)
#         list1 = [dataInt(x) for x in list1]
#         add_index(datas, list1, querydict)
#         saveToDisk([list1,querydict], file_querylist)
#     return  [list1,querydict]
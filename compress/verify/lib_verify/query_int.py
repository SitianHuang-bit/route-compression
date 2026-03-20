import math,sys
sys.path.append('..')
from lib import *
# from zip import *
# from verify import *

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

def query_int_ip2(ip: int, datas_dict: dict, querylist: list[dataInt], querydict: dict) -> list:
    """查询单条ip(int型)数据库的位置,这个是优化后的查询方法

    Args:
        ip (int): [description]
        datas (list[data]): [description]
        list_int (list[dataInt]): [description]

    Returns:
        tuple: 经纬度
    """
    tmp1 = 100000
    #如果那个值小于最小的
    flag = math.floor(ip/tmp1)
    value = querydict.get(flag)
    if value == None:
        while value == None:
            flag = flag + 1
            value = querydict.get(flag)
        value = [value[0],value[0]+1]

    tmp = binarySearch_query(querylist, value[0], value[1], ip)
    list_index = list(querylist[tmp].indexs)

    if len(list_index) == 0:
        return [360, 360]
    else:
       return [datas_dict[list_index[0]].lng, datas_dict[list_index[0]].lat]
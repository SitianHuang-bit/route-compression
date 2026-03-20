import sys

sys.path.append('../..')

from lib import *
import ipaddress

def getLocal(datas):
        """返回前缀更多的 data 经纬度
        """
        if ipaddress.ip_network(datas[0].iprefix).num_addresses \
            >= ipaddress.ip_network(datas[1].iprefix).num_addresses:
            return datas[0].lng, datas[0].lat
        else:
            return datas[1].lng, datas[1].lat


def mergeData_iprefix(*datas) -> data:
    """合并传入的 data

    Returns:
        data: [description]
    """
    datas = datas if len(datas) > 1 else datas[0]  #如果传入是 list
    iprifixs = [x.iprefix for x in datas]  # 前缀s

    # locals = [data.locals for data in datas]  #位置s

    # locals = []  #位置s
    # for x in datas:
    #     locals += x.locals

    iprifix = mergeIprefix2(iprifixs)  #合并前缀
    ipIndex, ipEnd = getIpStartEnd(iprifix)
    # local = mergeLocal(locals)  #合并位置
    local = getLocal(datas)
    return data(iprifix, datas[0].asn, local[0], local[1], ipIndex, ipEnd)


def mergeData_iprefix2(*datas) -> data:
    """合并传入的 data

    Returns:
        data: [description]
    """
    datas = datas if len(datas) > 1 else datas[0]  #如果传入是 list
    iprifixs = [x.iprefix for x in datas]  # 前缀s

    # locals = [data.locals for data in datas]  #位置s

    locals = []  #位置s
    for x in datas:
        locals += x.locals

    iprifix = mergeIprefix2(iprifixs)  #合并前缀
    ipIndex, ipEnd = getIpStartEnd(iprifix)
    local = mergeLocal(locals)  #合并位置
    return data(iprifix, datas[0].asn, local[0], local[1], ipIndex, ipEnd)


def mergeData_ipint(*datas)->list:
    """合并传入的 data

    Returns:
        data: [description]
    """
    datas = datas if len(datas) > 1 else datas[0]  #如果传入是 list

    locals = set()  #位置s
    for x in datas:
        locals = locals | x.locals #取两个集合的并集

    list1 = list(locals)
    local = mergeLocal(list1)  #合并位置
    #判断合并后的经纬度是否与它们相聚在规定的范围内
    for i in range(len(list1)):
         if distance(local[0], local[1], list1[i][0], list1[i][1]) > 1000:
             return [1,False] #代表不能进行压缩
    
    a = []
    for v in datas:
        a.append(v.ipIndex)
        a.append(v.ipEnd)
    data1 = data(datas[0].iprefix, datas[0].asn, local[0], local[1], min(a),
                max(a))
    data1.import_locals(locals)
    return [data1,True]  #代表可以压缩


def mergeData2_ipint(*datas) -> data:
    """合并传入的 data，取前缀范围更大 data 的经纬度

    Returns:
        data: [description]
    """
    datas = datas if len(datas) > 1 else datas[0]  #如果传入是 list

    local = getLocal(datas)

    a = []
    for v in datas:
        a.append(v.ipIndex)
        a.append(v.ipEnd)
    return data(datas[0].iprefix, datas[0].asn, local[0], local[1], min(a),
                max(a))
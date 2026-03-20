import sys,os
sys.path.append('../..')
from lib import *


def distance_data(data1: data, data2: data) -> float:
    """计算传入的两个data的距离

    Args:
        data1 (data): [description]
        data2 (data): [description]

    Returns:
        float: [description]
    """
    # print(data1.iprefix)
    return distance(data1.lng, data1.lat, data2.lng, data2.lat)

def setdiss(datas:list,file_diss:str)->list:
    """得到所有相邻前缀之间距离的集合，即diss集合

    Args:
        datas (list): 获取的zip集合
    """
    if os.path.exists(file_diss):
        diss = loadFromDisk(file_diss)
    else:
        diss = [
            distance_data(datas[i], datas[i + 1]) for i in range(len(datas) - 1)
        ]
        saveToDisk(diss, file_diss)  #所有距离保存在diss里
    return diss


def getMinIndex(diss,min_diss) -> int:
    """获取diss中最小值的下标

    Returns:
        int: [description]
    """
    return diss.index(min_diss)


def saveResult_len(datas,lens:list):
    """保存压缩结果
    """
    # lens = lens if len(lens) > 1 else lens[0]
    
    if len(datas) in lens:
        saveAllData(datas, "../data/zip/zip-%s.db" % len(datas))


def remove_anoma(diss:list,datas:list[data],range1:int) -> tuple:
    """去除异常数据，并返回异常数据和去除之后的数据

    Args:
        diss (list): [description]
        datas (list[data]): [description]

    Returns:
        [type]: 异常数据数组，去除异常数据数组
    """
    del_index = []
    del_datas = []
    for i in range(len(diss)-2):#获取异常数据
        print(datas[i].iprefix)
        if (diss[i] > range1) and (diss[i+1] > range1) and (distance_data(datas[i],datas[i+2]) <= range1):
            del_index.append(i+1)
            del_datas.append(datas[i+1])
    
    del_index.sort(reverse= True)#将下标数组倒序，因为删除要倒序删除
    for i in range(len(del_index)):#开始删除异常数据
        print(del_index[i])
        del datas[del_index[i]]

    return del_datas,datas
# setDatas()
# setdiss()

import math
from lib.binarySearch import *

def get_index(querylist:list[dataInt],querydict:dict,data1:data):
    tmp = 100000
    value_pre = querydict.get(math.floor(data1.ipIndex/tmp))
    value_last = querydict.get(math.floor(data1.ipEnd/tmp))    
    index_pre = binarySearch(querylist,value_pre[0],value_pre[1],data1.ipIndex)
    index_last = binarySearch(querylist,value_last[0],value_last[1],data1.ipEnd)
    return index_pre,index_last

def __get_min_prefix__(list_index:list,datas_dict:dict)->str:
    """返回最小区间范围的前缀

    Args:
        list_index (list): _description_
        datas_dict (dict): _description_

    Returns:
        str:返回前缀
    """
    list1 = []
    ##注意这个data应该是一个dict，通过key——value查找
    for i in range(len(list_index)):
        list1.append(datas_dict[list_index[i]])

    if len(list1) <= 0 or list1 == None:
        return 'ip'

    list1.sort(key=lambda data: data.ipEnd - data.ipIndex)

    return list1[0].iprefix

def get_iprefix_Interval(datas:list[data],querylist:list,querydict:dict,datas_dict:dict):
    
    new_datas = []
    for data in  datas:
        query_index = get_index(querylist,querydict,data)
        interval = []
        for i in range(query_index[0],query_index[1]):
            #中间一段区间的前一个数据的下标是i,list_index_pre是前后的index集合
            list_index_pre = list(querylist[i].indexs & querylist[i+1].indexs)
            #获取到最小区间的前缀
            tmp2 = __get_min_prefix__(list_index_pre,datas_dict)
            if tmp2 == 'ip': #如果原来没有查到，则后面不需要查询
                continue
            if tmp2 == data.iprefix:
                if querylist[i+1].number - querylist[i].number >1:
                    interval.append([querylist[i].number,querylist[i+1].number])
        new_datas.append([data,interval])
    return new_datas

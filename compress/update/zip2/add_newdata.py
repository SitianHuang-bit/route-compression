#更新压缩过程中需要用到的函数
# from algorithm_compress import *
import sys,os
sys.path.append('..')
from lib import *
from verify.lib_verify import *

tmp = 100000
def get_querylist3(datas:dict,file_querylist:str):
    """得到数据的中间查询数组
    Args:
        file (str): [description]

    Returns:
        list[dataInt]: [description]
    """
    if os.path.exists(file_querylist):
        tmp1 = loadFromDisk(file_querylist)
        querylist = tmp1[0]
        querydict = tmp1[1]
        querylist_number = tmp1[2]
    else:
        set1 = add_number(datas)
        querylist = list(set1)
        querylist.sort()
        querylist_number = querylist.copy() #只是所有的ipIndex和ipend排序
        querydict = querydict_(querylist)
        querylist = [dataInt(x) for x in querylist]
        add_index(datas, querylist, querydict)
        saveToDisk([querylist,querydict,querylist_number], file_querylist)
    return  [querylist,querydict,querylist_number]

def get_querylist3_1(datas:dict):
    """得到数据的中间查询数组
    Args:
        file (str): [description]

    Returns:
        list[dataInt]: [description]
    """
    set1 = add_number(datas)
    querylist = list(set1)
    querylist.sort()
    querylist_number = querylist.copy() #只是所有的ipIndex和ipend排序
    querydict = querydict_(querylist)
    querylist = [dataInt(x) for x in querylist]
    add_index(datas, querylist, querydict)
    return  [querylist,querydict,querylist_number]


def get_querylist2(datas:dict,querylist_number:list,file_querylist:str):
    """得到数据的中间查询数组
    Args:
        file (str): [description]

    Returns:
        list[dataInt]: [description]
    """
    if os.path.exists(file_querylist):
        querylist = loadFromDisk(file_querylist)[0]
        querydict = loadFromDisk(file_querylist)[1]
    else:
        if not isinstance(querylist_number, list):
            querylist_number = list(querylist_number)
            
        querydict = querydict_(querylist_number)
        querylist = [dataInt(x) for x in querylist_number]
        add_index(datas, querylist, querydict)
        saveToDisk([querylist,querydict], file_querylist)
    return  [querylist,querydict]

def get_querylist2_1(datas:dict,querylist_number:list):
    """得到数据的中间查询数组
    Args:
        file (str): [description]

    Returns:
        list[dataInt]: [description]
    """
    querydict = querydict_(querylist_number)
    querylist = [dataInt(x) for x in querylist_number]
    add_index(datas, querylist, querydict)
    return  [querylist,querydict]

def combined_datas(zip_result:list,zip_result_del:list):
    """合并原来压缩结果和剔除出来的压缩结果

    Args:
        zip_result (list): [description]
        zip_result_del (list): [description]
    """
    #合并
    zip_result += zip_result_del
    #将结果按照ipIndex排序
    return sorted(zip_result, key=__getIpStart__)


def re_datas(list1:list)->list[data]:
    """"重新构建新的前缀数据"""
    new_datas= []
    for i in range(len(list1)):
        for j in range(len(list1[i][1])):
            iprefix = list1[i][0].iprefix+"_"+str(j)
            new_datas.append(data(iprefix,list1[i][0].asn,list1[i][0].lng,list1[i][0].lat,list1[i][1][j][0],list1[i][1][j][1]))
    
    return new_datas

def get_new_datas(zip_del:list[data],datas_dict:dict,querylist:list,querydict:dict)->list[data]:
    #需要先获取到所有被调出来的数据的真实区间，然后再构建新的数据

    datas_del = get_iprefix_Interval(zip_del,querylist,querydict,datas_dict)
    #用datas_del重新构建新的datas
    new_del_datas = re_datas(datas_del)
    #给新的data赋值locals
    for i in new_del_datas:
        i.setlocals()
    return new_del_datas

        
def change_querylist(new_data:data,querylist:list[dataInt],querydict:dict,new_key:str):
    """更新querylist，将新区间的值插入到querylist中

    Args:
        new_data (_type_): _description_
        querylist (list[dataInt]): _description_
        querydict (dict): _description_
        new_key (str): _description_
    """
    #首先找到ipIndex在querylist中新插入的位置
    new_value_ipIndex = math.floor(new_data.ipIndex/tmp)
    value_pre = querydict.get(new_value_ipIndex)
    tmp1 = binarySearch(querylist,value_pre[0],value_pre[1],new_data.ipIndex)
    #找到ipEnd在querylist中新插入的位置
    new_value_ipEnd = math.floor(new_data.ipEnd/tmp)
    value_last = querydict.get(new_value_ipEnd)
    tmp2 = binarySearch(querylist,value_last[0],value_last[1],new_data.ipEnd)
    #将
    for i in range(tmp1,tmp2+1):
        querylist[i].addIndex(new_key)
        
# def change_querylist2(new_data:data,querylist:list[dataInt],querydict:dict,new_key:str):
#     """更新querylist，将新区间的值插入到querylist中

#     Args:
#         new_data (_type_): _description_
#         querylist (list[dataInt]): _description_
#         querydict (dict): _description_
#         new_key (str): _description_
#     """
#     #首先找到ipIndex在querylist中新插入的位置
#     new_value_ipIndex = math.floor(new_data.ipIndex/tmp)
#     value_pre = querydict.get(new_value_ipIndex)
#     tmp1 = binarySearch(querylist,value_pre[0],value_pre[1],new_data.ipIndex)
#     #找到ipEnd在querylist中新插入的位置
#     new_value_ipEnd = math.floor(new_data.ipEnd/tmp)
#     value_last = querydict.get(new_value_ipEnd)
#     tmp2 = binarySearch(querylist,value_last[0],value_last[1],new_data.ipEnd)
#     #将
#     for i in range(tmp1,tmp2+1):
#         querylist[i].indexs.discard(new_key)
    

def update(new_data:list[data],datas:list[data],diss:list,datas_dict:dict,querylist:list[dataInt],querydict:dict):
    """当来了一条新数据时，更新所有数据

    Args:
        new_data (data): [description]
        datas (list[data]): [description]
        diss (list): [description]
        datas_dict (dict): [description]
        query_initial (list): [description]
        querylist (list): [description]
        querydict (dict): [description]
    """
    #更新datas，将新数据插入已经排好序的datas中
    for data in new_data:
        new_index = binarySearch_data(datas,0,len(datas)-1,data.ipIndex)
        print(data.iprefix)
        datas.insert(new_index,data)
        #更新diss   用一个flag表示后续是否还需要压缩，如果不需要直接结束
        if new_index > 0: #插入的位置不是第一个
            d1 = distance(datas[new_index-1].lng,datas[new_index-1].lat,data.lng,data.lat)
            if new_index-1 == len(diss):
                diss.insert(new_index-1,d1)
            else:
                diss[new_index-1] = d1
        if new_index+1 < len(datas): #插入的位置不是最后一个
            d2 = distance(datas[new_index+1].lng,datas[new_index+1].lat,data.lng,data.lat)
            diss.insert(new_index,d2)
        #改变datas_dict
        datas_dict[str(len(datas_dict)+1)] = data
        #改变querylist
        change_querylist(data,querylist,querydict,str(len(datas_dict)))
    # return datas

def is_None(value_index:int,value,querydict:dict):
    while value==None:
        value_index -= 1
        value = querydict.get(value_index)
    value = [value[1],value[1]+1]
    return value


def change_querylist_querydict(new_data:data,querylist:list[dataInt],querydict:dict,new_key:str,remove_querylist:list[dataInt]):
    """更新querylist,将新区间的值插入到querylist中
    Args:
        new_data (_type_): _description_
        querylist (list[dataInt]): _description_
        querydict (dict): _description_
        new_key (str): _description_
    
    """
    pre_index,last_index = 0,0
    querydict_Max = math.floor(querylist[-1].number/tmp)
    #首先找到ipIndex在querylist中新插入的位置
    new_value_ipIndex = math.floor(new_data.ipIndex/tmp)
    value_pre = querydict.get(new_value_ipIndex)
    #由于存在处于临界值情况，因此需要向外扩一位
    if value_pre != None: 
        if value_pre[0]== 0 and value_pre[1]!=(len(querylist)-1):
            value_pre = [value_pre[0],value_pre[1]+1]
        elif value_pre[0]!= 0 and value_pre[1]==(len(querylist)-1):
            value_pre = [value_pre[0]-1,value_pre[1]]
        elif value_pre[0]!= 0 and value_pre[1]!=(len(querylist)-1):
            value_pre = [value_pre[0]-1,value_pre[1]+1]

    #如果要是空的话向下循环查找到真正存在的就行
    if value_pre == None:
        value_pre = is_None(new_value_ipIndex,value_pre,querydict)
    
    tmp1 = binarySearch2(querylist,value_pre[0],value_pre[1],new_data.ipIndex)
    #找到ipEnd在querylist中新插入的位置
    new_value_ipEnd = math.floor(new_data.ipEnd/tmp)
    value_last = querydict.get(new_value_ipEnd)
    if value_last == None:
        value_last = is_None(new_value_ipEnd,value_last,querydict)
    tmp2 = binarySearch2(querylist,value_last[0],value_last[1],new_data.ipEnd)
    
    if isinstance(tmp1, int) and isinstance(tmp2, int):
        pre_index = tmp1
        last_index = tmp2
    elif isinstance(tmp1, tuple) and isinstance(tmp2, int):
        pre_index = tmp1[1]
        #由于新插入了一个值，所以下标向后移动一位
        last_index = tmp2+1
        querylist.insert(pre_index,dataInt(new_data.ipIndex))
        if pre_index != 0 and pre_index !=(len(querylist)-1):
            querylist[pre_index].addIndex(querylist[pre_index-1].indexs & querylist[pre_index+1].indexs)
            
        #改变querydict，由于新插入了querylist因此需要改变querydict，为下一次的查找做准备
        if new_value_ipIndex in querydict:
            querydict[new_value_ipIndex][1] +=1
        else:#倘若不在，则新添加一个key——value对
            querydict[new_value_ipIndex] = [pre_index,pre_index]
        for  i in range(new_value_ipIndex+1,querydict_Max+1):
            if i in querydict:
                querydict[i][0] +=1
                querydict[i][1] +=1
                
        #更改原始压缩后形成的querylist
        remove_querylist.insert(pre_index,dataInt(new_data.ipIndex))
        if pre_index != 0 and pre_index !=(len(remove_querylist)-1):
            remove_querylist[pre_index].addIndex(remove_querylist[pre_index-1].indexs & remove_querylist[pre_index+1].indexs)


    elif isinstance(tmp1, int) and isinstance(tmp2, tuple):
        pre_index = tmp1
        last_index = tmp2[1]
        querylist.insert(last_index,dataInt(new_data.ipEnd))
        if last_index != 0 and last_index !=(len(querylist)-1):
            querylist[last_index].addIndex(querylist[last_index-1].indexs & querylist[last_index+1].indexs)
        #更改querydict
        if new_value_ipEnd in querydict:
            querydict[new_value_ipEnd][1] +=1
        else:#倘若不在，则新添加一个key——value对
            querydict[new_value_ipEnd] = [last_index,last_index]
        for i in range(new_value_ipEnd+1,querydict_Max+1):
            if i in querydict:
                querydict[i][0] +=1
                querydict[i][1] += 1



        #更改原始压缩后形成的querylist
        remove_querylist.insert(last_index,dataInt(new_data.ipEnd))
        if last_index != 0 and last_index !=(len(remove_querylist)-1):
            remove_querylist[last_index].addIndex(remove_querylist[last_index-1].indexs & remove_querylist[last_index+1].indexs)
        

    elif isinstance(tmp1, tuple) and isinstance(tmp2, tuple):
        pre_index = tmp1[1]
        last_index = tmp2[1]+1 #前面已经插入一个值，所以需要向后移动一位
        querylist.insert(pre_index,dataInt(new_data.ipIndex))
        if pre_index != 0 and pre_index != (len(querylist)-1):
            querylist[pre_index].addIndex(querylist[pre_index-1].indexs & querylist[pre_index+1].indexs)
        querylist.insert(last_index,dataInt(new_data.ipEnd))
        if last_index != 0 and last_index !=(len(querylist)-1):
            querylist[last_index].addIndex(querylist[last_index-1].indexs & querylist[last_index+1].indexs)
        
        #更改原始压缩后形成的querylist
        remove_querylist.insert(pre_index,dataInt(new_data.ipIndex))
        if pre_index != 0 and pre_index !=(len(remove_querylist)-1):
            remove_querylist[pre_index].addIndex(remove_querylist[pre_index-1].indexs & remove_querylist[pre_index+1].indexs)
        
        remove_querylist.insert(last_index,dataInt(new_data.ipEnd))
        if last_index != 0 and last_index !=(len(remove_querylist)-1):
            remove_querylist[last_index].addIndex(remove_querylist[last_index-1].indexs & remove_querylist[last_index+1].indexs)
       

        #更改querydict
        #如果新插入的ipIndex数据key值存在querydict中，就将其右侧数字加一
        if new_value_ipIndex in querydict:
            querydict[new_value_ipIndex][1] +=1
        else:#倘若不在，则新添加一个key——value对
            querydict[new_value_ipIndex] = [pre_index,pre_index]
        
        #之后将ipIndex的后一个key值到ipEnd的key值对应的所有区间全都加一
        for i in range(new_value_ipIndex+1 ,new_value_ipEnd+1):
            if i in querydict:
                querydict[i][0] +=1
                querydict[i][1] +=1

        #再判读ipEnd数据对应的key值是否存在，存在则将其右侧数字加一
        if new_value_ipEnd in querydict:
            querydict[new_value_ipEnd][1] +=1
        else:
            querydict[new_value_ipEnd] = [last_index,last_index]
        #再将ipEnd之后的key值对应的区间全部加二
        for i in range(new_value_ipEnd+1,querydict_Max+1):
            if i in querydict:
                querydict[i][0] +=2
                querydict[i][1] +=2

    #将新的key值挂上
    for i in range(pre_index,last_index+1):
        querylist[i].addIndex(new_key)






def initial_update(new_data:list[data],datas:list[data],datas_dict:dict,querylist:list[dataInt],querydict:dict,remove_querylist:list):
    """当来了一条新数据时，更新所有数据

    Args:
        new_data (data): [description]
        datas (list[data]): [description]
        diss (list): [description]
        datas_dict (dict): [description]
        query_initial (list): [description]
        querylist (list): [description]
        querydict (dict): [description]
    """
    #更新datas，将新数据插入已经排好序的datas中
    for data in new_data:
        new_index = binarySearch_data(datas,0,len(datas)-1,data.ipIndex)
        print(data.iprefix)
        datas.insert(new_index,data)
        #改变datas_dict
        datas_dict[str(len(datas_dict)+1)] = data
        #改变querylist和querydict
        change_querylist_querydict(data,querylist,querydict,str(len(datas_dict)),remove_querylist)
    return datas



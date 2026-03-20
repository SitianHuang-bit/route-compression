#提供压缩过程的所有算法
import math
from numpy import save
from zip.lib2 import *
import sys
sys.path.append('..')
from lib import *
from verify import *


# threshold = 200.000000  # 阈值距离，超过即视为异常数据

def checkSearchDatas(datas: list[data]) -> list:
    """返回网段最小的 data 的经纬度.

    Args:
        datas (list[data]): []

    Returns:
        tuple[float, float]: []
    """
    if len(datas) <= 0 or datas == None:
        return [360, 360]

    datas.sort(key=lambda data: data.ipEnd - data.ipIndex)
    if len(datas) >= 2 and (datas[1].ipEnd - datas[1].ipIndex == datas[0].ipEnd - datas[0].ipIndex):
        return [False]
    else:
        return [datas[0].lng, datas[0].lat,datas[0].locals]


def binarySearch(list1: list[dataInt], start: int, end: int, key: int) -> int:
    """二分查找找到list1[mid].number = key的值

    Args:
        list1 (list[dataInt]): [description]
        start (int): [description]
        end (int): [description]
        key (int): [description]
    """
    if end >= start:
        mid = int(start + (end - start) / 2)
        if list1[mid].number == key:
            return mid
        elif list1[mid].number > key:  # 中间值.number > key
            return binarySearch(list1, start, mid - 1, key)  # 向左查找
        else:  # 中间值.number <= key
            return binarySearch(list1, mid + 1, end, key)  # 向右查找
    else:
        return start

def binarySearch_data(datas: list[data], start: int, end: int, key: int) -> int:
    """二分查找找到list1[mid].number = key的值

    Args:
        list1 (list[dataInt]): [description]
        start (int): [description]
        end (int): [description]
        key (int): [description]
    """
    if end >= start:
        mid = int(start + (end - start) / 2)
        if datas[mid].ipIndex == key:
            return mid
        elif datas[mid].ipIndex > key:  # 中间值.number > key
            return binarySearch_data(datas, start, mid - 1, key)  # 向左查找
        else:  # 中间值.number <= key
            return binarySearch_data(datas, mid + 1, end, key)  # 向右查找
    else:
        return start

def add_dele(merged_data:list[data],querylist:list[dataInt],querydict:dict,datas_dict:dict,interval_new:list):
    """合并区间后，中间查询数组中删除原来的key，添加新的key

    Args:
        merged_data (list[dataInt]): [description]
        querylist_remove (list[dataInt]): [description]
        datas_remove_dict (dict): [description]
        interval_new (list): [description]

    Returns:
        list: [description]
    """
    #获取新插入的区间的两个下标 
    tmp = 100000
    value_pre = querydict.get(math.floor(interval_new[0]/tmp))
    value_last = querydict.get(math.floor(interval_new[1]/tmp))    
    index_pre = binarySearch(querylist,value_pre[0],value_pre[1],interval_new[0])
    index_last = binarySearch(querylist,value_last[0],value_last[1],interval_new[1])
    index_last2 = index_last
    #如果出现第二个数据ipEnd小于第一个数据的ipEnd，这样后面就不能查找到真正的第二个数据的key值了
    if merged_data[0].ipEnd > merged_data[1].ipEnd:
        tmp2 = querydict.get(math.floor(merged_data[1].ipEnd/tmp))
        index_last2 = binarySearch(querylist,tmp2[0],tmp2[1],merged_data[1].ipEnd)

    #首先获取到这两条数据对应的key值
    del_dict_Index = []
    for i in range(len(list(querylist[index_pre].indexs))):
        # a = list(querylist[index_pre].indexs)[i]
        # b = datas_dict[list(querylist[index_pre].indexs)[i]]
        # print(b == merged_data[0])
        if merged_data[0] == datas_dict[list(querylist[index_pre].indexs)[i]]:
            del_dict_Index.append(list(querylist[index_pre].indexs)[i])
            break

    for i in range(len(list(querylist[index_last2].indexs))):
        if merged_data[1] == datas_dict[list(querylist[index_last2].indexs)[i]]:
            del_dict_Index.append(list(querylist[index_last2].indexs)[i])
            break
    #删除原来的两个下标并添加新的下标
    # querylist_pre = copy.deepcopy(querylist[index_pre:index_last+1])

    for i in range(index_pre,index_last+1):
        querylist[i].indexs.discard(del_dict_Index[0])
        querylist[i].indexs.discard(del_dict_Index[1])
        querylist[i].indexs.add(str(len(datas_dict)))
    return [[index_pre,index_last],[[merged_data[0],del_dict_Index[0]],[merged_data[1],del_dict_Index[1]]]]

def insert_new(querylist:list[dataInt],datas_dict:dict,data_new:data,querydict:dict):
    """插入新区间，生成新data后，改变dict和中间查询数组querylist
    Args:
        querylist_remove (list[dataInt]): [description]
        datas_remove_dict (dict): [description]
        data_new (data): [description]
    """
    #新添加数据到dict中
    datas_dict[str(len(datas_dict)+1)] = data_new
    tmp = 100000
    value_pre = querydict.get(math.floor(data_new.ipIndex/tmp))
    value_last = querydict.get(math.floor(data_new.ipEnd/tmp))
    #新插入到中间查询数组querylist中
    ipIndex_ = binarySearch(querylist, value_pre[0], value_pre[1], data_new.ipIndex)
        # inEnd下标
    ipEnd_ = binarySearch(querylist, value_last[0], value_last[1], data_new.ipEnd)
        # 插入下标
    query_index(querylist, ipIndex_, ipEnd_, str(len(datas_dict))) #挂下标


def deal_datas_diss(datas:list,diss:list,minIndex:int,range1):
    #需要删除原来合并后保留下来的data
    datas.pop(minIndex + 1)
    # diss 处理
    diss.pop(minIndex)
    # diss 更新
    if minIndex > 0:
        diss[minIndex - 1] = distance_data(datas[minIndex - 1], datas[minIndex])
    if minIndex + 1 < len(datas):
        diss[minIndex] = distance_data(datas[minIndex], datas[minIndex + 1])
    
    # if minIndex > 0:
    #     if diss[minIndex - 1] != range1*100: #
    #         diss[minIndex - 1] = distance_data(datas[minIndex - 1], datas[minIndex])
    # if minIndex + 1 < len(datas):
    #     if diss[minIndex] !=range1*100:
    #         diss[minIndex] = distance_data(datas[minIndex], datas[minIndex + 1])

def get_lon_lat(list_index:list,datas_dict:dict):
    list1 = []
    ##注意这个data应该是一个dict，通过key——value查找
    for i in range(len(list_index)):
        list1.append(datas_dict[list_index[i]])

    return checkSearchDatas(list1)
    

#开始压缩
def com_algorithm(initial_datas_dict:dict,initial_querylist:list[dataInt],datas:list[data],diss:list,datas_dict:dict,querylist:list[dataInt],querydict:dict,range1:float,result_file:str)->list[data]:
    """压缩算法

    Args:
        datas(list): 要开始压缩的数据
        diss(list): 数据的每条相互之间的距离
        datas_remove_dict (dict): 将要压缩的数据变成dict
        querylist_remove (list): 生成中间查询数组
        file (str): 最终结果保存到的位置

    Returns:
        [type]: 最终压缩结果
    """
    new_iprefix = 0
    while len(datas) > 1:
        
        # saveResult_len(datas,[800000,700000,600000,500000,400000,300000,200000,160000,152800])
        print(len(datas))
        interval_new = [] #合并后区间
        merged_data = []  #要合并的两条数据
        #用于存放前后查询的经纬度
        new_data_list = [] #存放合并后收到影响的区间生成的新数据
        min_diss = min(diss)
        flag = True #判断是否由于合并后区间大小相同且有重叠问题造成的不能合并
        if min_diss <= 2*range1:
            minIndex = getMinIndex(diss,min_diss)
            
            com_data = mergeData_ipint(datas[minIndex], datas[minIndex + 1])
            if com_data[1]==True : #根据聚合后经纬度到原始经纬度的距离判断能否合并

                #得到合并前的两条数据
                merged_data.append(datas[minIndex])
                merged_data.append(datas[minIndex + 1])
                #将原始datas_dict和querylist保存下来，如果不能合并，则恢复

                #获取合并后区间
                interval_new.append(com_data[0].ipIndex)
                interval_new.append(com_data[0].ipEnd)
                #合并后处理dict
                datas_dict[str(len(datas_dict)+1)] = com_data[0]
                
                #合并后处理querylist  
                p = add_dele(merged_data,querylist,querydict,datas_dict,interval_new)
                interval_index = p[0] #querylist中受影响的那段的下标
                two_datas_dict = p[1] #受影响的那段querylist

                for i in range(interval_index[0],interval_index[1]):
                    location_pre_last = []
                    #中间一段区间的前一个数据的下标是i,list_index_pre是前后的index集合
                    #如果区间中间没有值的情况下，不需要查询,直接跳过
                    if initial_querylist[i].number + 1 == initial_querylist[i+1].number:
                        continue
                    else:
                        list_index_pre = list(initial_querylist[i].indexs & initial_querylist[i+1].indexs)
                        #获取到最小区间的经纬度
                        tmp2 = get_lon_lat(list_index_pre,initial_datas_dict)
                        if tmp2 == [360,360]: #如果原来没有查到，则后面不需要查询
                            continue
                        location_pre_last.append(tmp2)
                        
                        #同上，但是这是查询压缩之后数据
                        list_index_last = list(querylist[i].indexs & querylist[i+1].indexs)
                        t = get_lon_lat(list_index_last,datas_dict)
                        if t[0] == False:
                            flag= False
                            break #如果合并后存在两个区间大小相同的情况，则直接不进行压缩
                        else:
                            location_pre_last.append(t)

                        if distance(location_pre_last[0][0],location_pre_last[0][1],location_pre_last[1][0],location_pre_last[1][1]) > range1:
                            #受影响的区间生成新数据，并且添加locals
                            data_new = data(str(new_iprefix),0,location_pre_last[0][0],location_pre_last[0][1],initial_querylist[i].number,initial_querylist[i+1].number)
                            new_iprefix += 1
                            data_new.import_locals(location_pre_last[0][2])
                            new_data_list.append([data_new,i,i+1])
                            #question_interval记录的是收到影响的区间以及相应的经纬度 [number_pre,number_last,lon,lat]
                    
                if len(new_data_list) != 0 or flag==False:#如果没有受到影响的区间则，直接合并就好

                    if len(new_data_list) >= 2:
                        #合并受影响的区间，如果有些收到影响的区间连续连接并经纬度相同，则可以合并
                        len1 = len(new_data_list)-1
                        i = 0
                        while len1>0:
                            len1-=1
                            if (new_data_list[i][2] == new_data_list[i+1][1]) and (new_data_list[i][0].lng,new_data_list[i][0].lat) == (new_data_list[i+1][0].lng,new_data_list[i+1][0].lat):
                                #合并数据
                                new_data_list[i][0].ipEnd = new_data_list[i+1][0].ipEnd
                                new_data_list[i][2] = new_data_list[i+1][2]
                                new_data_list.pop(i+1)
                            else:
                                i+=1

                    #插入受影响的区间
                    if len(new_data_list) <= 1 and flag==True : #判定几个受影响区间可以合并并插入

                        #判断一下是否新插入的区间与原本的区间大小一样，如果一样认定不可聚合
                        if len(new_data_list) == 1:
                            new_interval = [new_data_list[0][0].ipIndex,new_data_list[0][0].ipEnd]
                            if ([merged_data[0].ipIndex,merged_data[0].ipEnd] ==new_interval)or([merged_data[1].ipIndex,merged_data[1].ipEnd] ==new_interval):
                                #相同则不聚合
                                #不能合并，还原datas_dict和querylist
                                for i in range(interval_index[0],interval_index[1]+1):
                                    if querylist[i].number >= two_datas_dict[0][0].ipIndex and querylist[i].number <=two_datas_dict[0][0].ipEnd:
                                        querylist[i].indexs.add(two_datas_dict[0][1])
                                    if querylist[i].number>= two_datas_dict[1][0].ipIndex and querylist[i].number <= two_datas_dict[1][0].ipEnd:
                                        querylist[i].indexs.add(two_datas_dict[1][1])
                                    querylist[i].indexs.discard(str(len(datas_dict)))
                                #还原datas_dict
                                del datas_dict[str(len(datas_dict))]
                                #并将目前diss中的距离变成大于range1的
                                diss[minIndex] = range1*200
                                continue
                        
                        datas[minIndex] = com_data[0]#用合并后的替换之前的data数据
                        #处理原来的datas和diss
                        deal_datas_diss(datas,diss,minIndex,range1)

                        #新插入的data数据，需要查找其再datas中的位置，从而改变diss中相应的距离
                        for i in range(len(new_data_list)):

                            new_index = binarySearch_data(datas,0,len(datas)-1,new_data_list[i][0].ipIndex)
                            datas.insert(new_index,new_data_list[i][0])
                            #更新diss
                            
                            t = diss[new_index-1]
                            if new_index >0: #不是放在第一个
                                # if  diss[new_index-1] != 1001:
                                diss[new_index-1] = distance(datas[new_index-1].lng,datas[new_index-1].lat,datas[new_index].lng,datas[new_index].lat)
                            if new_index +1 < len(datas): #不是放在最后一个
                                d2 = distance(datas[new_index+1].lng,datas[new_index+1].lat,datas[new_index].lng,datas[new_index].lat)
                                diss.insert(new_index,d2)
                            
                            # if new_index >0: #不是放在第一个
                            #     # if  diss[new_index-1] != 1001:
                            #     if new_index-minIndex == 1: #让新合并后的数据与新插入的数据标记为不能合并
                            #         diss[new_index-1] = range1*100
                            #     elif new_index-minIndex == 0 and t == range1*100:
                            #         diss[new_index-1] = range1*100
                            #     else:
                            #         diss[new_index-1] = distance(datas[new_index-1].lng,datas[new_index-1].lat,datas[new_index].lng,datas[new_index].lat)
                            # if new_index +1 < len(datas): #不是放在最后一个
                            #     if new_index-minIndex == 0: #让新合并后的数据与新插入的数据标记为不能合并
                            #         d2 = range1*100
                            #     elif new_index-minIndex == 1 and t == range1*100:
                            #         d2 = range1*100
                            #     else:
                            #         d2 = distance(datas[new_index+1].lng,datas[new_index+1].lat,datas[new_index].lng,datas[new_index].lat)
                            #     diss.insert(new_index,d2)

                            #改变dict和querylist  
                            datas_dict[str(len(datas_dict)+1)] = new_data_list[i][0]
                            query_index(querylist, new_data_list[i][1], new_data_list[i][2], str(len(datas_dict)))

                    else:
                        #不能合并，还原datas_dict和querylist
                        for i in range(interval_index[0],interval_index[1]+1):
                            if querylist[i].number >= two_datas_dict[0][0].ipIndex and querylist[i].number <=two_datas_dict[0][0].ipEnd:
                                querylist[i].indexs.add(two_datas_dict[0][1])
                            if querylist[i].number>= two_datas_dict[1][0].ipIndex and querylist[i].number <= two_datas_dict[1][0].ipEnd:
                                querylist[i].indexs.add(two_datas_dict[1][1])
                            querylist[i].indexs.discard(str(len(datas_dict)))
                        #还原datas_dict
                        del datas_dict[str(len(datas_dict))]
                        #并将目前diss中的距离变成大于range1的
                        diss[minIndex] = range1*200
                else:
                    datas[minIndex] = com_data[0]#用合并后的替换之前的data数据
                    #处理原来的datas和diss
                    deal_datas_diss(datas,diss,minIndex,range1)
            else:
                #将目前diss中的距离变成大于range1的
                diss[minIndex] = range1*200
        else:
            saveAllData(datas,result_file)
            # saveToDisk(datas,result_file)
            return datas
    return datas


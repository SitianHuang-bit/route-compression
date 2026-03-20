#增量压缩，直接将新增的数据合并到原始压缩完成的数据中，之后进行压缩
#这种方法适用于一次有很多的更新前缀的情况
from lib import *
from zip2.algorithm_compress import *
from zip2 import *

def __getIpStart__(elem: data):
    return elem.ipIndex

def del_same_interval(data1:data,querylist:list[dataInt],querydict:dict,datas_dict:dict):
    """判断是否存在相同区间的数据,如果存在返回该下标,不存在返回False
    """
    #获取新插入的区间的两个下标 
    tmp = 100000
    value_pre = querydict.get(math.floor(data1.ipIndex/tmp))
    value_last = querydict.get(math.floor(data1.ipEnd/tmp)) 
    if value_pre== None or value_last == None:
        return False
    index_pre = binarySearch2(querylist,value_pre[0],value_pre[1],data1.ipIndex)
    index_last = binarySearch2(querylist,value_last[0],value_last[1],data1.ipEnd)
    if isinstance(index_pre, int) and isinstance(index_last, int):
        #如果这两个值都存在，则需要判断这两个值上共同存在的区间范围是否等于该区间
        list_index = list(querylist[index_pre].indexs & querylist[index_last].indexs)
        #将这些包含该范围的区间是否与该区间正好相同
        for i in range(len(list_index)):
            if datas_dict[list_index[i]].ipIndex == data1.ipIndex and datas_dict[list_index[i]].ipEnd == data1.ipEnd:
                return int(list_index[i])
    else:
        return False
    #全部不相同，则返回False
    return False

def deal_same_interval(new_del_datas:list[data],zip_remove:list[data],zip_remove_querylist:list[dataInt],zip_remove_querydict:dict,zip_remove_dict:dict):
    #判断新的添加的数据与目前被压缩完成的数据中是否存在区间重复问题，存在的话，将原始数据中的删除掉
    del_index = []
    for i in range(len(new_del_datas)):
        t = del_same_interval(new_del_datas[i],zip_remove_querylist,zip_remove_querydict,zip_remove_dict)
        if t!= False:
            del_index.append(t)
    #删除数据的同时还要删除相应的diss中的数据
    del_index.sort(reverse = True)
    for i in range(len(del_index)):
        #处理数据
        del zip_remove[del_index[i]]
    return zip_remove

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

#获取新数据，这个新数据是原来不存在的前缀
new_datas = getAllDB('G:/前缀压缩/BGP/BGP/Main/data_del/datas_del.db')

#获取原始数据加上新数据的总和
#来的前缀全部都是新生成的前缀，目前没有的前缀，并且也已经确定好位置
initial_datas = getDatas("G:/前缀压缩/BGP/BGP/Main/data_remove/datas_remove.db")#数据
#合并数据
initial_datas = combined_datas(initial_datas,new_datas)
#从新生成许多的数据，data_dict,querylist,querydict等
initial_datas_dict = setdict(initial_datas)  #将数据变成dict
initial_query = get_querylist3(initial_datas_dict,"G:/前缀压缩/BGP/BGP/Main/data_remove/query_datas_remove")
initial_querylist = initial_query[0] #生成中间查询数组
initial_querydict = initial_query[1] #生成中间查询字典
initial_querylist_number = initial_query[2] #生成中间查询数组中的单纯数字

#需要先获取到所有被调出来的数据的真实区间
#获取新来数据的真实区间并生成相应的data
re_new_datas = get_new_datas(new_datas,initial_datas_dict,initial_querylist,initial_querydict)


#合并之前判断情一下原始数据中是否存在与新的前缀区间重合况，如果存在需要记录下来并删除之后才能合并
zip_remove = loadFromDisk('G:/前缀压缩/BGP/BGP/Main/data_remove/zip1000/zip_remove')
zip_remove_dict = setdict(zip_remove)
zip_remove_query = get_querylist3(zip_remove_dict,"G:/前缀压缩/BGP/BGP/Main/data_remove/zip1000/query_zip_remove1")
zip_remove_querylist = zip_remove_query[0]
zip_remove_querydict = zip_remove_query[1]

#处理原始压缩数据中与新数据重合的区间数据
zip_remove = deal_same_interval(re_new_datas,zip_remove,zip_remove_querylist,zip_remove_querydict,zip_remove_dict)

#合并
data_combined = combined_datas(zip_remove,re_new_datas)
#将结果保存
# saveAllData(data_combined,"./data_combined/data_combined.db")
#开始进行压缩，分别从新计算出来diss,datas_dict,querylist,querydict等数据
diss = setdiss(data_combined,'G:/前缀压缩/BGP/BGP/Main/data_combined/data_combined_diss.db')
data_combined_dict = setdict(data_combined)
data_combined_query = get_querylist2(data_combined_dict,initial_querylist_number,"G:/前缀压缩/BGP/BGP/Main/data_combined/combined_query")
data_combined_querylist = data_combined_query[0]
data_combined_number = data_combined_query[1]


data_combined_querydict = querydict_(data_combined_number)
zip = com_algorithm(initial_datas_dict,initial_querylist,data_combined,diss,data_combined_dict,data_combined_querylist,data_combined_querydict,1000,'./data_combined/zip1000/data_combined1000','./data_combined/zip1000/data_combined_diss')



pass

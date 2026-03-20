from lib import *
from zip2.algorithm_compress import *
from zip2 import *
def check_del_prefix_type(del_data: data, zip_datas: list[data]) -> str:
    """判断被删除前缀的类型
    Args:
        del_data: 被删除的前缀
        zip_datas: 压缩后的前缀列表
    Returns:
        str: INTERNAL/START/END/INDEPENDENT
    """
    for zip_data in zip_datas:
        # 内部前缀
        if (del_data.ipIndex > zip_data.ipIndex) and (del_data.ipEnd < zip_data.ipEnd):
            return "INTERNAL"
        # 起始前缀    
        if (del_data.ipIndex == zip_data.ipIndex) and (del_data.ipEnd < zip_data.ipEnd):
            return "START"
        # 末尾前缀    
        if (del_data.ipIndex > zip_data.ipIndex) and (del_data.ipEnd == zip_data.ipEnd):
            return "END"
    # 独立前缀
    return "INDEPENDENT"


def find_zip_data(del_data: data, zip_datas: list[data], type: str) -> data:
    """找到删除前缀对应的压缩后区间
    Args:
        del_data: 被删除的前缀
        zip_datas: 压缩后的前缀列表
        type: START/END
    Returns:
        data: 对应的压缩后区间
    """
    for zip_data in zip_datas:
        if type == "START" and del_data.ipIndex == zip_data.ipIndex:
            return zip_data
        if type == "END" and del_data.ipEnd == zip_data.ipEnd:
            return zip_data
    return None

def update_query_structure(del_data: data, querylist: list[dataInt], querydict: dict, operation: str):
    """更新查询结构
    Args:
        del_data: 被删除的前缀
        querylist: 查询列表
        querydict: 查询字典
        operation: remove/update
    """
    # 获取查询区间的范围
    tmp = 100000
    value_pre = querydict.get(math.floor(del_data.ipIndex/tmp))
    value_last = querydict.get(math.floor(del_data.ipEnd/tmp))
    for key in querydict:
        print(f"Key: {key}, Value: {querydict[key]}")
    if value_pre is None or value_last is None:
        return
        
    # 获取索引
    index_pre = binarySearch2(querylist, value_pre[0], value_pre[1], del_data.ipIndex)
    index_last = binarySearch2(querylist, value_last[0], value_last[1], del_data.ipEnd)
    
    # 处理起始索引
    start_index = index_pre[1] if isinstance(index_pre, tuple) else index_pre
    # 处理结束索引
    end_index = index_last[1] if isinstance(index_last, tuple) else index_last

    # # 使用处理后的索引
    # for i in range(start_index, end_index+1):
    #     print(querylist[i].indexs)
    #     if querylist[i].number >= del_data.ipIndex and querylist[i].number <= del_data.ipEnd:
    #         querylist[i].indexs.discard(str(del_data.ipIndex))
    i = start_index
    while i <= end_index:
        if querylist[i].number >= del_data.ipIndex and querylist[i].number <= del_data.ipEnd:
            # 从 querylist 中删除元素
            del querylist[i]
            # 如果删除了一个元素，end_index 要减小 1，因为列表长度会缩短
            end_index -= 1
            # 删除一个元素后，i 不自增，因为删除的元素已被移除，i 会指向下一个元素
            continue
        i += 1


def remove_data(del_data: data, zip_datas: list[data]):
    """从压缩后数据中移除独立前缀
    Args:
        del_data: 要删除的前缀
        zip_datas: 压缩后的前缀列表
    """
    for i, zip_data in enumerate(zip_datas):
        if zip_data.ipIndex == del_data.ipIndex and zip_data.ipEnd == del_data.ipEnd:
            zip_datas.pop(i)
            break
            
def update_diss(zip_datas: list[data]) -> list:
    """更新距离矩阵
    Args:
        zip_datas: 压缩后的前缀列表
    Returns:
        list: 更新后的距离矩阵
    """
    zip_datas.sort(key=lambda x: x.ipIndex)
    print(f"Number of zip_datas: {len(zip_datas)}")
    
    diss = []
    if len(zip_datas) <= 1:
        return diss
        
    for i in range(len(zip_datas)-1):
        dist = distance(zip_datas[i].lng, zip_datas[i].lat,
                       zip_datas[i+1].lng, zip_datas[i+1].lat)
        diss.append(dist)
    print(f"Length of diss: {len(diss)}")
    return diss

def get_next_prefix_start(del_data: data, initial_datas: list[data]) -> int:
    """找到被删除前缀在原始数据中的下一条前缀的起始位置
    Args:
        del_data: 被删除的前缀
        initial_datas: 原始未压缩的前缀列表
    Returns:
        int: 下一条前缀的起始位置
    """
    for data in initial_datas:
        if data.ipIndex > del_data.ipIndex:  # 找到第一条起始位置大于被删除前缀的前缀
            return data.ipIndex
    return del_data.ipEnd + 1  # 如果没找到，则返回删除前缀的结束位置+1

def delete_algorithm(initial_datas: list[data], 
                    del_datas: list[data],
                    zip_datas: list[data],
                    querylist: list[dataInt],
                    querydict: dict,
                    datas_dict: dict) -> list[data]:
    need_recompress = False
    
    for del_data in del_datas:
        del_type = check_del_prefix_type(del_data, zip_datas)
        print(del_type)
        if del_type == "INTERNAL":
            update_query_structure(del_data, querylist, querydict, "remove")
            
        elif del_type == "START":
            zip_data = find_zip_data(del_data, zip_datas, "START")
            if zip_data:
                # 找到原始数据中的下一条前缀的起始位置
                next_start = get_next_prefix_start(del_data, initial_datas)
                zip_data.ipIndex = next_start  # 更新为下一条前缀的起始位置
                update_query_structure(del_data, querylist, querydict, "remove")
                
        elif del_type == "END":
            zip_data = find_zip_data(del_data, zip_datas, "END")
            if zip_data:
                zip_data.ipEnd = del_data.ipIndex - 1
                update_query_structure(del_data, querylist, querydict, "remove")
                
        else:  # INDEPENDENT
            remove_data(del_data, zip_datas)
            #初始前缀list
            initial_datas[:] = [data for data in initial_datas if data.iprefix != del_data.iprefix]
            #初始前缀dict
            initial_datas_dict = setdict(initial_datas)
            initial_query = get_querylist(initial_datas_dict, "G:/前缀压缩/BGP_del/BGP/Main/data_del/initial/initial_query_1")
            initial_querylist = initial_query[0]
            initial_querydict = initial_query[1]
            #压缩后的前缀list
            datas_dict = setdict(zip_datas)
            zip_query = get_querylist(datas_dict, "G:/前缀压缩/BGP_del/BGP/Main/data_del/initial/zip_query_1")
            querylist = zip_query[0]
            querydict = zip_query[1]
            #update_query_structure(del_data, querylist, querydict, "remove")
            need_recompress = True
    
    if need_recompress:
        zip_datas.sort(key=lambda x: x.ipIndex)
        diss = update_diss(zip_datas)
        print("Detailed info before com_algorithm:")
        for i, data in enumerate(zip_datas):
            print(f"zip_datas[{i}]: ipIndex={data.ipIndex}, ipEnd={data.ipEnd}, lng={data.lng}, lat={data.lat}")
        print("diss values:", diss)
        for idx, data in enumerate(querylist):
            print(f"querylist[{idx}].number = {data.number}")
            print(f"querylist[{idx}].indexs = {data.indexs}")
        for key in initial_datas_dict:
            print(f"Key: {key}, Value: {initial_datas_dict[key].iprefix}")

        for key in datas_dict:
            print(f"Key: {key}, Value: {datas_dict[key].iprefix}")
        return com_algorithm(initial_datas_dict, initial_querylist,
                        zip_datas, diss, datas_dict,
                        querylist, querydict, 1000, "result_path")
    
    return zip_datas


# 1. 加载需要的数据
# 加载原始未压缩数据
initial_datas = getDatas("G:/前缀压缩/BGP_del/BGP/Main/v_bgps/data/zips_2025.db")
initial_datas_dict = setdict(initial_datas)
initial_query = get_querylist(initial_datas_dict, "G:/前缀压缩/BGP_del/BGP/Main/data_del/initial/initial_query")
initial_querylist = initial_query[0]
initial_querydict = initial_query[1]

# 2. 加载压缩后的数据
zip_datas = getDatas('G:/前缀压缩/BGP_del/BGP/Main/data_del/finaltest_2025.db')  # 加载已经压缩的数据
zip_datas_dict = setdict(zip_datas)

zip_query = get_querylist(zip_datas_dict, "G:/前缀压缩/BGP_del/BGP/Main/data_del/initial/zip_query")
zip_querylist = zip_query[0]
zip_querydict = zip_query[1]

# 3. 加载要删除的数据
del_datas = getAllDB('/data/datas_del_2025.db')  # 要删除的前缀数据

# 4. 调用删除算法
result = delete_algorithm(initial_datas,      # 压缩前的前缀
                         del_datas,           # 要删除的前缀
                         zip_datas,           # 压缩后的前缀
                         zip_querylist,       # 查询列表
                         zip_querydict,       # 查询字典
                         zip_datas_dict)      # 数据字典

# 5. 保存结果
saveAllData(result, 'G:/前缀压缩/BGP_del/BGP/Main/data_del/datas_del_result_2025.db')
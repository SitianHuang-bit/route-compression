from lib.bgp_class import *

# def binarySearch(list1: list[dataInt], start: int, end: int, key: int) -> int:
#     """二分查找找到list1[mid].number = key的值

#     Args:
#         list1 (list[dataInt]): [description]
#         start (int): [description]
#         end (int): [description]
#         key (int): [description]
#     """
#     if end >= start:
#         mid = int(start + (end - start) / 2)
#         if list1[mid].number == key:
#             return mid
#         elif list1[mid].number > key:  # 中间值.number > key
#             return binarySearch(list1, start, mid - 1, key)  # 向左查找
#         else:  # 中间值.number <= key
#             return binarySearch(list1, mid + 1, end, key)  # 向右查找
#     else:
#         return start
def binarySearchBig(list1: list[dataInt], start: int, end: int, key: int) -> int:
    """二分查找找到list1[mid].number = key的值

    Args:
        list1 (list[dataInt]): [description]
        start (int): [description]
        end (int): [description]
        key (int): [description]
    """
    if start <= end:
        mid = start + (end - start) // 2
        if list1[mid].number == key:
            # 继续向右查找以确定是否有重复且下标更大的相同元素
            larger_index = binarySearchBig(list1, mid + 1, end, key)
            return larger_index if larger_index != -1 else mid
        elif list1[mid].number > key:
            return binarySearchBig(list1, start, mid - 1, key)
        else:
            return binarySearchBig(list1, mid + 1, end, key)
    else:
        return -1

def binarySearchSmall(list1: list[dataInt], start: int, end: int, key: int) -> int:
    """二分查找找到list1中key的最小索引

    Args:
        list1 (list[dataInt]): 有序列表，其中的元素具有 'number' 属性
        start (int): 查找的起始索引
        end (int): 查找的结束索引
        key (int): 要查找的键值

    Returns:
        int: 键值在列表中的最小索引
    """
    if end >= start:
        mid = start + (end - start) // 2
        if list1[mid].number == key:
            # 继续向左查找以确定是否有重复且下标更小的相同元素
            smaller_index = binarySearchSmall(list1, start, mid - 1, key)
            return smaller_index if smaller_index != -1 else mid
        elif list1[mid].number > key:
            return binarySearchSmall(list1, start, mid - 1, key)
        else:
            return binarySearchSmall(list1, mid + 1, end, key)
    else:
        return -1  # 仅在递归查找中使用，最终结果不会是-1
    
    
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

def binarySearch2(list1: list[dataInt], start: int, end: int, key: int):
    """二分查找找到list1[mid].number = key或与key相邻的两个数据对应的下标

    Args:
        list1 (list[dataInt]): [description]
        start (int): [description]
        end (int): [description]
        key (int): [description]

    Returns:
        flag用来表示：key是否已经存在list中，如果存在则是1，不存在则是-1
    """
    if end >= start:
        mid = int(start + (end - start) / 2)
        if list1[mid].number == key:
            return mid
        if list1[mid].number > key:  # 中间值.number > key
            return binarySearch2(list1, start, mid - 1, key)  # 向左查找
        else:  # 中间值.number <= key
            return binarySearch2(list1, mid + 1, end, key)  # 向右查找
    else:
        return (start - 1, start)

def binarySearch_query(list1: list[dataInt], start: int, end: int, key: int):
    """二分查找找到list1[mid].number = key或与key相邻的两个数据对应的下标

    Args:
        list1 (list[dataInt]): [description]
        start (int): [description]
        end (int): [description]
        key (int): [description]

    Returns:
        flag用来表示：key是否已经存在list中，如果存在则是1，不存在则是-1
    """
    while end >= start:
        mid = int(start + (end - start) / 2)
        if list1[mid].number == key:
            return mid
        elif list1[mid].number > key:  # 中间值.number > key
            end = mid-1  # 向左查找
        else:  # 中间值.number <= key
            start = mid+1  # 向右查找
    
    return start- 1
from multiprocessing import Pool
import os, time
import multiprocessing

__maxCores__ = multiprocessing.cpu_count() #最大线程数


def mutualProcess(func, arglist: list) -> bool:
    """多进程处理，成功返回true 失败 false

    Args:
        func ([函数]): [进程处理入口函数]
        arglist (list): [函数参数list] 

    Returns:
        bool: [判断运行结果]
    """
    if arglist == []: return False  # 如果参数list 为空

    start = time.time()
    tasks = len(arglist)  #任务数

    p = Pool(__maxCores__)  #初始化进程池

    for i in range(tasks):
        p.apply_async(func, arglist[i])
    p.close()
    p.join()  #等待所有任务结束

    end = time.time()
    print('时间花费', end - start)

    return True

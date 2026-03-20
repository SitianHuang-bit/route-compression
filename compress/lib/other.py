import pickle, os

import nvector as nv

def saveToDisk(instance, fileName: str = 'instance'):
    """保存对象实例

    Args:
        instance ([type]): [对象实例]
        fileName (str, optional): [文件路径]. Defaults to 'instance'.
    """
    file = open(fileName, 'wb')
    pickle.dump(instance, file)
    file.close


def loadFromDisk(fileName: str = 'instance'):
    """加载对象实例

    Args:
        fileName (str, optional): [description]. Defaults to 'instance'.

    Returns:
        [type]: [description]
    """
    with open(fileName, 'rb') as file:
        instance = pickle.load(file)
    return instance


def init_Instance(file: str, func, *args, **args2):
    """返回实例对象,如果本地存在则读取本地,否则执行func创建

    Args:
        file (str): [本地实例]
        func ([type]): [创建实例函数]

    Returns:
        [type]: [实例对象]
    """
    if os.path.exists(file):
        instance = loadFromDisk(file)
    else:
        instance = func(*args, **args2)
        saveToDisk(instance, file)
    return instance

    


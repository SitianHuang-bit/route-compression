# from lib_verify import *
import sys
sys.path.append('..')
from lib import *

def getIps(n: int , dbfile: str = '') -> list:
    """返回 dbfile 每个前缀下 n 个 int 类型 ips
    Args:
        n (int, optional): [description]. Defaults to 10.

    Returns:
        list: [description]
    """
    datas = getAllDB(dbfile)

    a = []
    for data in datas:
        a += ipaddresss_data(data, n)

    return a

def getResult_prefix(query, base) ->list:
    """计算传入的query与base之间的相同ip定位的距离

    Args:
        query ([type]): [description]
        base ([type]): [description]

    Returns:
        list: [ip,距离]
    """
    # base = [0, base] if len(base) > 2 else base
    a = []
    for i, v in enumerate(query):
        if base[i].ip == v.ip:
            b = distance(base[i].lng, base[i].lat, v.lng, v.lat)
            # a.append(b)
            # a.append([base[i].ip,b])
            print(intToAddress(base[i].ip))
            if not b == 0:
                s = "ip:" +intToAddress(base[1][i].ip) + " " + str(base[1][i].ip) + " "\
                    "local: %s,%s base: %s,%s distance %s" % (v.lng, v.lat, base[1][i].lng, base[1][i].lat, b)
                a.append([b,s])
                print(s)

    return a

def getResult_int(query, base):
    """计算与传入 base 的经纬度距离

    Args:
        query ([type]): [description]
        base ([type]): [description]

    Returns:
        [type]: [description]
    """
    base = [0, base] if len(base) > 2 else base
    a = []
    c = []
    for i, v in enumerate(query):
        if base[1][i].flag == True and v.flag == True \
            and base[1][i].ip == v.ip:
            b = distance(base[1][i].lng, base[1][i].lat, v.lng, v.lat)
            a.append(
                [v.ip, b, (v.lng, v.lat), (base[1][i].lng, base[1][i].lat)])
            print(base[1][i].ip)
        else:
            c.append([v,base[1][i]])
            # if not b == 0:
            #     s = "ip:" +intToAddress(base[1][i].ip) + " " + str(base[1][i].ip) + " "\
            #         "local: %s,%s base: %s,%s distance %s" % (v.lng, v.lat, base[1][i].lng, base[1][i].lat, b)
            #     tmp.append(s)
            #     print(s)

    return [a,c]


def getfail(query:list,base:list)->list:
    """获取两个数组中相同ip下经纬度不同的经纬度

    Args:
        query (list): [description]
        base (list): [description]

    Returns:
        list: ip+原始经纬度+压缩后经纬度
    """
    a = []
    for i, v in enumerate(query):
        if base[i].ip == v.ip:
            if base[i].lng != v.lng or base[i].lat != v.lat:
                a.append([base[i].ip,(base[i].lng,base[i].lat),(v.lng,v.lat)])
    
    return a
              



import ipaddress, random
from netaddr import cidr_merge
from bitarray import bitarray
import re

from lib.bgp_class import data

__ipNumber__ = 2147483647  # ipv4 最大 int 值

# def __getNumbers__(n: int):
#     a = int(__ipNumber__ / n) - 1
#     return range(1, __ipNumber__, a)


def intToAddress(ipN: int) -> str:
    """ip int 类型转换 十进制字符串表示

    Args:
        ipN (int): [int 类型 ip]

    Returns:
        str: [十进制 ip str]
    """
    return str(ipaddress.ip_address(ipN))




def addressToInt(ipA: str) -> int:
    """ip 十进制字符串转换成 int 类型

    Args:
        ipA (str): [十进制 ip 字符串]

    Returns:
        int: [ip int 数值]
    """
    return int(ipaddress.ip_address(ipA))

def ipaddresss_data(data:data, m:int) -> list[int]:
    """返回前缀下 m 个 ip 地址

    Args:
        iprefix (str): [description]
        m (int, optional): [description]. Defaults to 10.

    Returns:
        list[str]: [description]
    """
    start, end = data.ipIndex,data.ipEnd

    if end-start > 2147483647:
        return []
    try:
        if end-start < 4: #将/30,/31,/32去掉
            return []
        elif end-start-1 <= m: 
            return [x for x in range(start+1, end)]
        else:
            return [random.randint(start+1, end-1) for x in range(m)]
    except Exception as e:
        return []

def ipaddresss(iprefix: str, m:int) -> list[int]:
    """返回前缀下 m 个 ip 地址

    Args:
        iprefix (str): [description]
        m (int, optional): [description]. Defaults to 10.

    Returns:
        list[str]: [description]
    """
    network = ipaddress.ip_network(iprefix)

    if network.num_addresses > 2147483647:
        return []

    start, end = getIpStartEnd(iprefix)
    
    try:
        if start == end:
            return [start]
        elif start == end-1:
            if m==1:
                return [start]
            else:
                return [start, end]
        elif end-start < m:
            return [x for x in range(start+1, end)]
        else:
            return [random.randint(start+1, end-1) for x in range(m)]
    except Exception as e:
        return []

def ip_all_addresss(iprefix: str) -> list[int]:
    """返回前缀下所有ip地址

    Args:
        iprefix (str): [description]
        m (int, optional): [description]. Defaults to 10.

    Returns:
        list[str]: [description]
    """
    network = ipaddress.ip_network(iprefix)

    if network.num_addresses > 2147483647:
        return []

    start, end = getIpStartEnd(iprefix)
    ips= []
    
    try:
        if start == end:
            return [start]
        elif start == end-1:
            return [start, end]
        else:
            return [x for x in range(start+1, end)]
    except Exception as e:
        return []

def getIpStartEnd(iprefix: str) -> tuple:
    """返回前缀下第一个和最后一个ip地址的 int 类型
    """
    start, end = 0, 0
    network = ipaddress.ip_network(iprefix)
    prefixlen = network.prefixlen
    for x in network.hosts():
        if prefixlen==31:
            start = int(x)
            end = start + int(network.num_addresses)-1
        elif prefixlen==32:
            start = int(x)
            end = start 
        else:
            start = int(x)-1
            end = start + int(network.num_addresses)-1
        break
    return start, end

def getIpStart(iprefix: str) -> int:
    """返回前缀下第一个和最后一个ip地址的 int 类型
    """
    start, end = 0, 0
    network = ipaddress.ip_network(iprefix)
    prefixlen = network.prefixlen
    for x in network.hosts():
        if prefixlen==31:
            start = int(x)
            end = start + int(network.num_addresses)-1
        elif prefixlen==32:
            start = int(x)
            end = start 
        else:
            start = int(x)-1
            end = start + int(network.num_addresses)-1
        break
    return start
def getIpEnd(iprefix: str) -> int:
    """返回前缀下第一个和最后一个ip地址的 int 类型
    """
    start, end = 0, 0
    network = ipaddress.ip_network(iprefix)
    prefixlen = network.prefixlen
    for x in network.hosts():
        if prefixlen==31:
            start = int(x)
            end = start + int(network.num_addresses)-1
        elif prefixlen==32:
            start = int(x)
            end = start 
        else:
            start = int(x)-1
            end = start + int(network.num_addresses)-1
        break
    return end
    
ipre = re.compile(r'(.*)\/(\d{1,2})')


def __getIpMask__(iprefix: str) -> tuple:
    """拆包子网,为 ip 和 mask 1.0.0.1/24 拆成 1.0.0.1 和 /24

    Args:
        iprefix (str): [description]

    Returns:
        tuple: [description]
    """
    a = ipre.findall(iprefix)
    return a[0][0], int(a[0][1])


def __getIpBin__(ip: int) -> str:
    """ip 转换为32位二进制字符串

    Args:
        ip (int): [description]

    Returns:
        str: [description]
    """
    a = str(bin(ip))[2:]
    b = 32 - len(a)
    return '0' * b + a


def mergeIprefix(*iprefixs) -> str:
    """合并传入的前缀,调用 netaddr -> cidr_merge ,严格意义上的前缀聚合.结果非常不好.
       iprefixs = ['1.0.0.0/24', '1.0.4.0/22', '1.0.4.0/24', '1.0.5.0/24','1.0.6.0/24', '1.0.7.0/24']
       只能聚合成 '1.0.0.0/24'.
    """
    iprefixs = iprefixs if len(iprefixs) > 1 else iprefixs[0]  #如果传入是 list

    iprefixs = iprefixs if type(
        iprefixs[0]) == str else [intToAddress(iptmp)
                                  for iptmp in iprefixs]  #如果传入的是 list[int]

    return str(cidr_merge(iprefixs)[0].cidr)


def mergeIprefix2(*iprefixs) -> str:
    """合并传入的前缀 非严格
       iprefixs = ['1.0.0.0/24', '1.0.4.0/22', '1.0.4.0/24', '1.0.5.0/24','1.0.6.0/24', '1.0.7.0/24']
    """
    def __getNewMask__() -> int:
        """从左向右,诸位比较,直到第一个不同的位置,返回.获取新前缀 Newmask

        Returns:
            int: [description]
        """
        for i in range(0, mask):
            a = ipbs[0][i]
            for ipb in ipbs:
                if not a == ipb[i]:
                    return i
        return mask

    iprefixs = iprefixs if len(iprefixs) > 1 else iprefixs[0]  #如果传入是 list
    iprefixs = iprefixs if type(
        iprefixs[0]) == str else [intToAddress(iptmp)
                                  for iptmp in iprefixs]  #如果传入的是 list[int]

    ips, masks = [], []  # 初始化
    for iprefix in iprefixs:
        a = __getIpMask__(iprefix)
        ips.append(addressToInt(a[0]))  # ipstr -> int
        masks.append(a[1])

    mask = min(masks)  # 最小掩码
    ipbs = [bitarray(__getIpBin__(ip))
            for ip in ips]  # int -> 32*二进制 -> bitarray

    nMask = __getNewMask__()  #newMask
    nIp_str = (ipbs[0][:nMask] +
               (32 - nMask) * bitarray('0')).to01()  #补全 32*二进制 -> ip_str

    return "%s/%s" % (intToAddress(int(nIp_str, 2)), nMask)
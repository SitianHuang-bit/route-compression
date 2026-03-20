#!/usr/bin/python3
from .bgp_class import localda
from .network import intToAddress, addressToInt
import geoip2.database, logging
import os
import lib
from pandas import DataFrame

libpath = os.path.dirname(lib.__file__)  #获取 lib 路径

geoipfile = os.path.join(libpath,
                         './geoip/GeoLite2-City.mmdb')  #拼接 GeoLite2-City.mmdb

# geoipfile = "./geoip/GeoLite2-City.mmdb"

read = geoip2.database.Reader(geoipfile)


def locations(ips: list) -> list:
    """返回一组 ip 地址经纬度

    Args:
        ips (list[str] or list[int]): [description]

    Returns:
        list: [description]
    """
    ips = ips if type(
        ips[0]) == str else [intToAddress(iptmp) for iptmp in ips]

    return [localda(addressToInt(x), 360, 360, *location(x)) for x in ips]

def locations2(ips: list) -> list:
    """返回一组 ip 地址经纬度

    Args:
        ips (list[str]): [description]

    Returns:
        list: [description]
    """
    if ips == []: return []
    ips = ips if type(
        ips[0]) == str else [intToAddress(iptmp) for iptmp in ips]

    return [location(x) for x in ips]

def locations3(ips: list):
    """返回一组 ip 地址经纬度

    Args:
        ips (list[str]): [description]
    Returns:
        list: [description]
    """
    if ips == []: return []
    ips = ips if type(
         ips[0]) == str else [intToAddress(iptmp) for iptmp in ips]
    print(ips[0])
    df = DataFrame(ips,columns=['ips'])

    return df['ips'].apply(location_).to_list()

def location(ipstr: str) -> tuple:
    """返回 ip 经纬度

    Args:
        ip (str): [ip地址]

    Returns:
        tuple: [经度,纬度]
    """
    # print(ipstr)
    try:
        response = read.city(ipstr)
        a = (response.location.longitude, response.location.latitude)
    except Exception as e:
        logging.exception(e)
        a = ()
    return a

def location_(ipstr: str) -> list:
    """返回 ip 经纬度

    Args:
        ip (str): [ip地址]

    Returns:
        tuple: [经度,纬度]
    """
    # print(ipstr)
    try:
        response = read.city(ipstr)
        a = (response.location.longitude, response.location.latitude)
    except Exception as e:
        logging.exception(e)
        a = ()
    return [addressToInt(ipstr),a]
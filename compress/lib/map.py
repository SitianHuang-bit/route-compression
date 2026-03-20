import nvector as nv
import numpy as np
import numpy.linalg as lin

__frame_E__ = nv.FrameE(a=6371e3, f=0)  #取地球直径 6371e3


def distance(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
    """返回两个坐标的距离 km.取地球标准球形,计算圆弧长度


    Args:
        lng1 (float): [description]
        lat1 (float): [description]
        lng2 (float): [description]
        lat2 (float): [description]

    Returns:
        float: [km]
    """
    positionA = __frame_E__.GeoPoint(lat1, lng1, degrees=True)
    positionB = __frame_E__.GeoPoint(lat2, lng2, degrees=True)

    path = nv.GeoPath(positionA, positionB)
    return path.track_distance(method='greatcircle') / 1000


def mergeLocal(*locals) -> tuple:
    """求传入地理位置的中心点坐标,直接取球状中心而非地理位置
    代码来自 https://pypi.org/project/nvector/#Example7:“Mean position”

    Returns:
        [type]: [description]
    """
    locals = locals if len(locals) > 1 else locals[0]  #如果传入是 list
    longitude, latitude = [], []
    for local in locals:
        # print(local)
        longitude += [local[0]]
        latitude  += [local[1]]
    points = nv.GeoPoint(latitude, longitude, degrees=True)
    nvectors = points.to_nvector()
    n_EM_E = nvectors.mean()
    g_EM_E = n_EM_E.to_geo_point()
    lat, lon = g_EM_E.latitude_deg, g_EM_E.longitude_deg
    lat, lon = round(lat, 4), round(lon, 4)  #保留4位小数
    return lon, lat

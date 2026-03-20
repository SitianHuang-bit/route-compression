import sqlite3
from .bgp_class import data


def __getIpStart__(elem: data):
    return elem.ipIndex

def getIpStart_(elem: data):
    return elem.ipIndex


__ipv4_table__ = '''CREATE TABLE IF NOT EXISTS ipv4
    (prefix KEY,
    asn NUMBER,
    lng NUMBER,
    lat NUMBER,
    ipindex NUMBER,
    ipend NUMBER);
    '''


def __init_db__(db: sqlite3.Connection, tablesql: str):
    """初始化表

    Args:
        db (sqlite3.Connection): [db]
        tablesql (str): [建表语句]
    """
    db.execute(tablesql)
    db.commit()


def __insert_s__(db: sqlite3.Connection, data):
    """插入/更新 ipv4 数据s
    """
    db.executemany('INSERT OR REPLACE INTO ipv4 VALUES (?,?,?,?,?,?)', data)


def __insert__(db: sqlite3.Connection, data):
    """插入/更新 ipv4 数据
    """
    db.executemany('INSERT OR REPLACE INTO ipv4 VALUES (?,?,?,?,?.?)',
                   (data, ))


def __save__(db: sqlite3.Connection, backupfile: str = "ipv4.db"):
    """保存数据库到硬盘

    Args:
        db (sqlite3.Connection): [前缀内存数据库]
        backupfile (str, optional): [备份文件路径]. Defaults to "ipv4.db".
    """
    db.commit()
    con = sqlite3.connect(backupfile)
    with con:
        db.backup(con)
    con.close()


def getAllDB(dbfile: str) -> list[data]:
    """获取数据库数据转换成 veda,按照 IpStart 排序

    Args:
        dbfile (str): [数据库文件路径]

    Returns:
        list[data]: [datas]
    """
    db = sqlite3.connect(dbfile)
    cur = db.execute("select * from ipv4 order by ipindex")
    c = [list(x) for x in cur.fetchall()]  # 获取全部数据
    d = [data(x[0], x[1], x[2], x[3], x[4], x[5]) for x in c]
    for i in d:
        i.setlocals()
    return sorted(d, key=__getIpStart__)

def getAllData(dbfile: str) -> list[data]:
    """获取数据库数据转换成 datas

    Args:
        dbfile (str): [数据库文件路径]

    Returns:
        list[data]: [datas]
    """
    db = sqlite3.connect(dbfile)
    cur = db.execute("select * from ipv4 order by ipindex")
    c = [list(x) for x in cur.fetchall()]  # 获取全部数据
    d = [data(x[0], x[1], x[2], x[3], x[4], x[5]) for x in c]
    return sorted(d, key=__getIpStart__)

def getAllData2(dbfile: str) -> list[data]:
    """获取数据库数据转换成 datas

    Args:
        dbfile (str): [数据库文件路径]

    Returns:
        list[data]: [datas]
    """
    db = sqlite3.connect(dbfile)
    cur = db.execute("select * from ipv4 order by ipindex")
    c = [list(x) for x in cur.fetchall()]  # 获取全部数据
    d = [data(x[0], x[1], x[2], x[3], x[4], x[5]) for x in c]
    return d



def saveAllData(datas: list[data], backupfile: str):
    """保存datas 到文件

    Args:
        datas (list[data]): [description]
        backupfile (str): [description]
    """
    c = [[x.iprefix, x.asn, x.lng, x.lat, x.ipIndex, x.ipEnd] for x in datas]
    db = sqlite3.connect(":memory:")  #内存数据库
    __init_db__(db, __ipv4_table__)
    __insert_s__(db, c)
    __save__(db, backupfile)  #保存到文件
    db.close()

def getDatas(file_zip:str) -> list[data]:
    """获取数据集，排除异常数据

    Args:
        file_zip (str): [description]

    Returns:
        [type]: [description]
    """
    datas = getAllDB(file_zip)  #获取数据
    datas = [data for data in datas
            if data.lat != None and data.lng != None]  #处理异常数据
    return datas

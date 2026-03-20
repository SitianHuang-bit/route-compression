class data():
    """
    数据库条目 基础数据结构
    """
    def __init__(self, iprefix: str, asn: int, lng: float, lat: float,
                 ipIndex: int, ipEnd: int):
        self.iprefix, self.asn = iprefix, asn
        self.lng, self.lat = lng, lat
        self.ipIndex, self.ipEnd = ipIndex, ipEnd
        # self.locals = [(lng, lat)]  #存储合并过程全部的经纬度
        self.locals = set() # data 实例化时，locals 初始化为空列表
        
    # def updatelocals(self,locals1,locals2): # 原始经纬度列表
    #     self.locals = locals1 + locals2
    def setlocals(self):
        self.locals.add((self.lng, self.lat))

    def import_locals(self,a):
        if type(a) == set:  #a 是 index set
            self.locals = self.locals | a
        else:  #单个 index
            self.locals.add(a)


class localda():
    """local 基础数据结构
    """
    def __init__(self, ip, lng: float = 360, lat: float = 360,*local):
        self.ip = ip
        if local == () or local == None:
            self.lng, self.lat = lng, lat
        else:
            self.lng, self.lat  = local[0], local[1]
        
        if self.lat == 360 or self.lng == 360 or self.lat == None or self.lng == None:
            self.flag = False

        else:
            self.flag = True

class dataInt():
    """
    查询时需要的数据结构
    """
    def __init__(self, number: int):
        self.number = number
        self.indexs = set()

    def addIndex(self, a):
        """叠加 index

        Args:
            a ([type]): [description]
        """
        if type(a) == set:  #a 是 index set
            self.indexs = self.indexs | a
        else:  #单个 index
            self.indexs.add(a)
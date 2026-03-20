#移除异常数据
import sys
import random
from lib import *
from zip import *
from verify import *

datas = getDatas("/data/zips_2022.db")
diss = setdiss(datas,"/data/diss")#得到diss，每条相互之间的距离
tmp = remove_anoma(diss,datas,2000)
datas_remove = tmp[1] #得到去除异常数据的数组
del_datas  = tmp[0]  #bei
saveAllData(datas_remove,"G:/前缀压缩/BGP/BGP/Main/data_remove/datas_remove.db")#保存去除异常数据的数组
saveAllData(del_datas,"G:/前缀压缩/BGP/BGP/Main/data_del/datas_del.db") #保存异常数据

pass


# datas =[    data('1.0.0.0/24', 13335, 143, -33.494, 1, 5),
#             data('1.0.0.1/24', 13335, 10, -33.494, 5, 8),
#             data('1.0.0.2/24', 13335, 142, -33.494, 14, 25),
#             data('1.0.0.3/24', 13335, 150, -33.494, 9, 12),
#             data('1.0.0.4/24', 13335, 143.2104, -33.494, 15, 17),
#             data('1.0.0.5/24', 13335, 143.2104, -33.494, 20, 23),
#             data('1.0.5.0/22', 13335, 143.2104, -33.494, 20, 25),
#             data('1.0.138.0/24', 23969, 104.1308, -33.494, 22, 24),
#             data('1.0.170.0/24', 23969, 143.9701, -33.494, 21, 25)
            
#             ]
# diss = setdiss(datas,"./data_move/diss")
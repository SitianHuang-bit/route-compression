from lib import *
from compress.zip.algorithm_compress_IPv4 import *
from verify import *
from zip.lib2 import *

data_file = ''
output_file = ''

#直接压缩数据
datas = getDatas("data_file")#获取数据
diss = setdiss(datas,"./data/diss")   #获取距离
datas_dict = setdict(datas)  #将数据变成dict
mid_query = get_querylist(datas_dict,"./data/query_zip2022")
querylist = mid_query[0] #生成中间查询数组
querydict = mid_query[1] #生成中间查询字典

initial_datas_dict = datas_dict.copy()
initial_querylist = get_querylist(datas_dict,"./data/query_zip2022")[0]

zip = com_algorithm(initial_datas_dict,initial_querylist,datas,diss,datas_dict,querylist,querydict,1000,'output_file')



pass
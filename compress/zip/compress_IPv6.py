from lib import *
from compress.zip.algorithm_compress_IPv6 import *
from verify import *
from zip.lib2 import *

#压缩去除异常数据的数据

# datas_remove = getDatas("./data_remove/datas_remove.db")#数据
# diss_remove = setdiss(datas_remove,"./data_remove/diss_remove")   #距离
# datas_remove_dict = setdict(datas_remove)  #将数据变成dict
# tmp = get_querylist(datas_remove_dict,"./data_remove/query_remove")
# querylist_remove = tmp[0] #生成中间查询数组
# querydict_remove = tmp[1] #生成中间查询字典

# initial_datas_dict = datas_remove_dict.copy()
# initial_querylist = get_querylist(datas_remove_dict,"./data_remove/query_remove")[0]

# zip_datas_remove = com_algorithm(initial_datas_dict,initial_querylist,datas_remove,diss_remove,datas_remove_dict,querylist_remove,querydict_remove,1000,'./data_remove/zip1000/zip_remove','./data_remove/zip1000/zip_remove_diss1000')


# # 直接压缩zip数据
datas = getDatas("G:/前缀压缩/BGP_ipv6/v_bgps/data/zip_2023_1.db")#数据  list[data]
diss = setdiss(datas,"G:/前缀压缩/BGP_ipv6/data/diss")   #距离   list  距离单位为km

datas_dict = setdict(datas)  #将数据变成dict   
mid_query = get_querylist(datas_dict,"G:/前缀压缩/BGP_ipv6/data/query_zip2023")
querylist = mid_query[0] #生成中间查询数组
querydict = mid_query[1] #生成中间查询字典

initial_datas_dict = datas_dict.copy()
initial_querylist = get_querylist(datas_dict,"G:/前缀压缩/BGP_ipv6/data/query_zip2023")[0]

zip = com_algorithm(initial_datas_dict,initial_querylist,datas,diss,datas_dict,querylist,querydict,1000,'G:/前缀压缩/BGP_ipv6/v_bgps/data/discard/null_datas_ipv6.db')


# saveToDisk(zip,'G:/前缀压缩/BGP_ipv6/v_bgps/data/123.db')

# pass
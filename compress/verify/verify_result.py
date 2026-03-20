#利用查询验证压缩前后距离是否在规定范围内
from lib_verify import *

ips = init_Instance("./data/ips", getIps, 1, './data/zip2022.db')  # 创建查询的 ips
original_queryResult = init_Instance('../data/result/original_queryResult',query_int,ips,'../data/zips_2022.db','../data/query_2022')
compress_queryResult = init_Instance('../data/result/compress_queryResult',query_int,ips,'../data/zip1000/zip1000.db','../data/zip1000/zip1000_query')
result_distance = init_Instance('../data/result/distance_change2',getResult_int,compress_queryResult, original_queryResult)

a = result_distance[0] #存放的是所有能查到结果的ip的结果
b = result_distance[1] #没有查询出经纬度的查询结果

#确认是否所有距离都在1000km以内
j=0
max = 0
fail_ips_zip_zip4 = []
for i in range(len(a)):
    # if a[i][1]>max:
    #     max = a[i][1]
    if(a[i][1] > 1000):
        j+=1
        fail_ips_zip_zip4.append(a[i][0])
        print([a[i][0],a[i][1],a[i][2],a[i][3]])
print(j)
# print(max)
pass


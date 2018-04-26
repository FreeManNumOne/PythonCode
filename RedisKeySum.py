#!/usr/bin/env python
#-*- coding:utf-8 -*-

#导入redis模块
import redis
import sys

r=redis.Redis(host='192.168.246.128',port=6379,password='test123456') #连接redis
keys=r.keys() #获取所有的keys
KeyWorld=sys.argv[1] #传入查询keys的关键字

#查询key关键字有多少个不过期的
KeysSum=0
for i in keys:
    #print(i)
    KeyExpir=r.ttl(i)
    if KeyExpir > 0:
        continue
    else:
        pass
        #print(i)
    if KeyWorld in i :
        KeysSum +=1
        print(i)

print("%s key 的总和是 %s"%(KeyWorld,KeysSum))

#KeyTypeList=[]
#for i in keys:
#    KeyType=r.type(i)
#    KeyTypeList.append(KeyType)
#KeyTypeListOne= list(set(KeyTypeList))
#print("去除重复后的Redis数据类型 %s"%KeyTypeListOne)


#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  redis
import  sys
import  time

#传入要删除key的文件
KeysFiles=sys.argv[1]

#连接redis以及打开要删除key的文件
#r=redis.Redis(host='192.168.246.128',port=6379,password="test123456")
r=redis.Redis(host='192.168.246.128',port=6379)#连接redis
Keys=open(KeysFiles,'r')
DelKeys=Keys.readlines()


#删除key逻辑
counter=0
DelKeysBatch=[]
for i in DelKeys:
    counter += 1
    DelKeysBatch.append(i.strip())
    if counter == 1000: #如果已经执行删除1000个key然后sleep 20秒
        r.delete(DelKeysBatch)
        time.sleep(20)
        counter = 0
    else:
        continue

#关闭要删除keys的文件
Keys.close()


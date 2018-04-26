#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  redis
import  sys
import  time

#传入要删除key的文件
KeysFiles=sys.argv[1]

#连接redis以及打开要删除key的文件
r=redis.Redis(host='192.168.246.128',port=6379,password="test123456")
Keys=open(KeysFiles,'r')
DelKeys=Keys.readlines()
r.client_list()

#删除key逻辑
counter=0
for i in DelKeys:
    r.delete(i.strip())    #删除key
    counter += 1
    if counter == 6000:   #如果已经执行删除5000的key程序sleep 20秒
        time.sleep(20)
        counter = 0
    else:
        continue

#关闭要删除keys的文件
Keys.close()


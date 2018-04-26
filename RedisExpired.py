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


#设置key的过期
counter=0
for i in DelKeys:
    r.expire(i,20)   #设置key的过期
    counter += 1
    if counter == 5000:   #如果已经执行设置key的过期5000的key程序sleep 20秒
        time.sleep(20)
        counter = 0
    else:
        continue

#关闭要删除keys的文件
Keys.close()


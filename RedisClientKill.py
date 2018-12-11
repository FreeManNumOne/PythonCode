#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  redis
import  sys

class RedisClientKills(object):
    def __init__(self,RedisServerIp,RedisServerPort,RedisPassWord):
        # 连接redis
        self.r = redis.Redis(host=RedisServerIp, port=RedisServerPort, password=RedisPassWord)
        # 获取Redis连接
        self.ClientList = self.r.client_list()

    def ClientKill(self):

        # kill连接空闲时间超过三天的连接
        for i in self.ClientList:
            IdleTime = i['idle']
            if int(IdleTime) > 259200:
                IdleSession = i['addr']
                self.r.client_kill(IdleSession)
                print('空闲连接：%s 被kill掉'%IdleSession)

    def QueryClient(self):
        # 查询空闲超过三天的连接
        for i in self.ClientList:
            IdleTime = i['idle']
            if int(IdleTime) > 259200:
                print('Idel 超过三天的连接',i)


if __name__ == "__main__":
    print("""
             python RedisClientKill.py redis服务器IP  Redis服务端口 Redis密码 传入的参数kill或者query
             示例： python RedisClientKill.py 192.168.200.195 6379 TestPasssword (kill or query)
            """)

    RedisServerIp = sys.argv[1]
    RedisServerPort = sys.argv[2]
    RedisServerPassword=sys.argv[3]
    Parameter = sys.argv[4]

    #实例化Redis连接
    RCK=RedisClientKills(RedisServerIp,RedisServerPort,RedisServerPassword)

    if Parameter == "query":
        #调用查询redis连接的方法
        RCK.QueryClient()
    elif Parameter == "kill":
        #调用杀掉redis连接的方法
        RCK.ClientKill()


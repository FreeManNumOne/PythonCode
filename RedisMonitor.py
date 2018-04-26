#!/usr/bin/env python
#-*- coding:utf-8 -*-

import  json
import  os
import  time
#微信发送告警模块
import socket
from send import *
from common import *
import RedisClientKill



class RedisMonitor(object):
    #Redis服务器连接信息
    def __init__(self):
        self.RedisServerPools=['172.19.69.224','172.19.69.203','172.19.69.204']
        self.RedisPort=6379
        self.RedisSentinelPort=26379
        self.RedisPassWord='namibankredisPord8ik,>LO(0p;/'

    #执行redis命令并返回结果
    def RedisCmd(self,command):
        CommandDone=os.popen(command).readlines()
        return CommandDone

    #获取当前那个是主Redis服务器
    def GetRedisMaster(self):
        for i in self.RedisServerPools:
            #print (i)
            cmd='redis-cli -h %s -p %s -a "%s" info Sentinel'%(i,self.RedisSentinelPort,self.RedisPassWord)
            CmdDone=self.RedisCmd(cmd)
            #print (CmdDone)
            if len(CmdDone) == 0 :
                continue
            RedisMasterIp=CmdDone[-1].split(',')[2].split('=')[1].split(':')[0]
            #print (RedisMasterIp)
            return  RedisMasterIp

    #获取当前主redis服务的info信息
    def GetRedisMonitorData(self):
        ReturRedisMasterIp=self.GetRedisMaster()
        cmd='redis-cli -h %s -p %s -a "%s" info '%(ReturRedisMasterIp,self.RedisPort,self.RedisPassWord)
        RedisMasterInfo=self.RedisCmd(cmd)
        #print(RedisMasterInfo)
        return  RedisMasterInfo

    #Redis 服务存活监控
    def RedisDown(self):
        for i in self.RedisServerPools:
            #print (i)
            cmd='redis-cli -h %s -p %s -a "%s" ping'%(i,self.RedisPort,self.RedisPassWord)
            CmdDone=self.RedisCmd(cmd)
            if len(CmdDone) ==0 :
                print ('严重:%s redise 节点Down机请尽快处理'%i)
                context = '严重:%s redise 节点Down机请尽快处理'%i
                self.WexixinSendMess('Redis节点down机', context)
                return
            if CmdDone[0].strip() != 'PONG':
                print ('严重:%s redise 节点Down机请尽快处理'%i)
                context = '严重:%s redise 节点Down机请尽快处理'%i
                self.WexixinSendMess('Redis节点down机', context)

    #哨兵服务存活监控
    def RedisSentinelDown(self):
        for i in self.RedisServerPools:
            #print (i)
            cmd='redis-cli -h %s -p %s -a "%s" ping'%(i,self.RedisSentinelPort,self.RedisPassWord)
            CmdDone=self.RedisCmd(cmd)
            if len(CmdDone) == 0 :
                #print ('严重:%s 哨兵节点Down机请尽快处理'%i)
                context = '严重:%s 哨兵节点Down机请尽快处理'%i
                self.WexixinSendMess('Redis哨兵节点down机', context)
                return
            if CmdDone[0].strip() != 'PONG':
                #print ('严重:%s 哨兵节点Down机请尽快处理'%i)
                context = '严重:%s 哨兵节点Down机请尽快处理'%i
                self.WexixinSendMess('Redis哨兵节点down机', context)

    #Redis主服务连接数监控
    def Connections(self):
        ConnectionsWarning=4000
        ConnectionsSum=self.GetRedisMonitorData()
        for i in ConnectionsSum:
            if 'connected_clients' in i :
                if int(i.split(':')[1])> int(ConnectionsWarning):
                    print('警告:Redis连接数大于1400 目前连接数为 %s， 请关注Redis主节点的机器性能'%i.split(':')[1].strip())
                    context ='警告:Redis连接数大于4000 目前连接数为 %s， 请关注Redis主节点的机器性能'%i.split(':')[1].strip()
                    self.WexixinSendMess('Redis连接数较大', context)
                    #self.ClientIdleKill()

    def ClientIdleKill(self):
        RedisServerIp = self.GetRedisMaster()
        RCK = RedisClientKill.RedisClientKills(RedisServerIp, self.RedisPort, self.RedisPassWord)
        RCK.ClientKill()
        context = '警告:%s Redis 空闲超过三天的连接已被client kill' %RedisServerIp
        self.WexixinSendMess('Redis空闲超过三天的连接已被kill', context)
        for i in self.RedisServerPools:
            RCK = RedisClientKill.RedisClientKills(i, self.RedisSentinelPort, self.RedisPassWord)
            RCK.ClientKill()
            context = '警告:%s Redis 空闲超过三天的连接已被client kill' % i
            self.WexixinSendMess('Redis空闲超过三天的连接已被kill', context)


    #Redis主服务key总和监控
    def SumsKeys(self):
        DbSzieWarning=3000000
        ReturRedisMasterIp = self.GetRedisMaster()
        cmd = 'redis-cli -h %s -p %s -a "%s" DBSIZE ' % (ReturRedisMasterIp, self.RedisPort, self.RedisPassWord)
        RedisMasterDbsize = self.RedisCmd(cmd)
        if int(RedisMasterDbsize[0].strip()) > int(DbSzieWarning):
            #print ('警告:Redis总KEY数大于2000，目前值 %s 请关注这个%s节点的机器性能'%(RedisMasterDbsize[0].strip(),ReturRedisMasterIp))
            context = '警告:Redis总KEY数大于300W，目前值 %s 请关注这个%s节点的机器性能'%(RedisMasterDbsize[0].strip(),ReturRedisMasterIp)
            self.WexixinSendMess('Redis总key数较大', context)

    #Redis在一定时间内发生主从切换监控
    def RedisMasterSwitch(self):
        LastMasterRedis=self.GetRedisMaster()
        time.sleep(5)
        NowRedisMaster=self.GetRedisMaster()
        if LastMasterRedis != NowRedisMaster:
            #print ('警告:Redis主节点发生切换，目前主节点是：%s'%NowRedisMaster)
            context = '警告:Redis主节点发生切换，目前主节点是：%s'%NowRedisMaster
            self.WexixinSendMess('Redis主从发切换', context)

    #Redis从节点数量监控
    def RedisSlaveDown(self):
        RedisSlaveWarning = 2
        RedisSlaveSum = self.GetRedisMonitorData()
        for i in RedisSlaveSum:
            if 'connected_slaves' in i:
                if int(i.split(':')[1]) < int(RedisSlaveWarning):
                    #print('警告:Redis从节点小于2，目前有 %s 个从节点 请检查Redis主从同步是否正常'%i.split(':')[1].strip())
                    context = '警告:Redis从节点小于2，目前有 %s 个从节点 请检查Redis主从同步是否正常'%i.split(':')[1].strip()
                    self.WexixinSendMess('Redis从节点小于1', context)

    #Redis使用系统内存情况进行监控
    def RedisMemory(self):
        RedisMemoryWarning= 2
        for redisip in self.RedisServerPools:
            #print (i)
            cmd='redis-cli -h %s -p %s -a "%s" info Memory'%(redisip,self.RedisPort,self.RedisPassWord)
            MemorySum=self.RedisCmd(cmd)
            for i in MemorySum:
                if 'used_memory_human' in i :
                    #print (i)
                    MemoryKey=i.split(':')[0]
                    MemoryValue=i.split(':')[1]
                    if  'G' in MemoryValue:
                        #print ('-->usermemory',i)
                        if int(MemoryValue.split(".")[0]) > int(RedisMemoryWarning):
                            context='警告:RedisServer %s 内存大于2G请检查这台机器内存以及性能' %redisip
                            self.WexixinSendMess('Redis使用内存告警',context)
    #Redis每秒执行命令监控
    def RedisCommandSec(self):
        RedisCommandSecWarning=13000
        RedisCommandSec = self.GetRedisMonitorData()
        for i in RedisCommandSec:
            if 'instantaneous_ops_per_sec' in i:
                if int(i.split(':')[1]) > int(RedisCommandSecWarning):
                    # print('警告:Redis现在每秒执行命令超过5500 目前每秒执行命令值为 %s， 请关注Redis主节点的机器性能'%i.split(':')[1].strip())
                    context = '警告:Redis现在每秒执行命令超过1.3W 目前每秒执行命令值为 %s， 请关注Redis主节点的机器性能'%i.split(':')[1].strip()
                    self.WexixinSendMess('Redis每秒执行命令超过告警阀值', context)

    #调用外部微信通道接口发送告警信息
    def WexixinSendMess(self,title,context):
        access_token = get_redis_token('http_check_token')
        user = 'daijh|yangke|yongjianzhuang|sunweiqiang|zhaohe'
        payload = qy_wx_msg(title, context, user)
        reload(sys)
        sys.setdefaultencoding('utf8')
        res = send_qy_msg(access_token, payload)

    # Redis使用系统内存情况进行监控
    def RedisSystemMemory(self):
         RedisSystemMemoryWarning = 2
         for redisip in self.RedisServerPools:
                # print (i)
                cmd = 'redis-cli -h %s -p %s -a "%s" info Memory' % (redisip, self.RedisPort, self.RedisPassWord)
                MemorySum = self.RedisCmd(cmd)
                for i in MemorySum:
                    if 'used_memory_rss' in i:
                        #print (i)
                        MemoryKey = i.split(':')[0]
                        MemoryValue = i.split(':')[1]
                        if 'G' in MemoryValue:
                                #print ('-->usermemory',)
                                #print ('memory',MemoryValue.split(".")[0])
                                if int(MemoryValue.split(".")[0]) > int(RedisSystemMemoryWarning):
                                      #print ('memory',MemoryValue.split(".")[0])
                                      context = '警告:RedisServer %s 使用系统内存大于2G请检查这台机器内存以及性能' % redisip
                                      self.WexixinSendMess('Redis使用系统内存告警', context)

if __name__ == "__main__":
    RedisMonitorRun=RedisMonitor()
    RedisMonitorRun.RedisDown()
    RedisMonitorRun.RedisSentinelDown()
    RedisMonitorRun.SumsKeys()
    RedisMonitorRun.Connections()
    RedisMonitorRun.RedisMasterSwitch()
    RedisMonitorRun.RedisSlaveDown()
    RedisMonitorRun.RedisMemory()
    RedisMonitorRun.RedisCommandSec()
    RedisMonitorRun.RedisSystemMemory()

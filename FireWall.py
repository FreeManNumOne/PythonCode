#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import datetime
import commands
import logging
import  time

#防火墙开通日志记录
def log(info):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/FireWall/logs/FireWallRecord.log',
                    filemode='a')
    logging.info(info)

# 添加iptables策略
def AddIptables(SourceIp, TargetIp):
    if 'list' in TargetIp:
        IptablesId = commands.getoutput('iptables --line-numbers  -L FORWARD  |grep %s | grep %s | wc -l' % (SourceIp, TargetIp))
        if int(IptablesId) == 0:
            os.popen('iptables -A FORWARD  -s %s -m set --match-set %s dst -j ACCEPT' % (SourceIp, TargetIp))
            log('策略开通成功 from %s to %s ' % (SourceIp,TargetIp))
            return 'sucess'
        else:
            return 'sucess'
    else:
        IptablesId = commands.getoutput('iptables --line-numbers  -L FORWARD  |grep %s | grep %s | wc -l' % (SourceIp, TargetIp))
        if int(IptablesId) == 0:
            cmd = 'iptables -A FORWARD -s %s -p tcp -d %s -j ACCEPT' % (SourceIp, TargetIp)
            commands.getoutput(cmd)
            log('策略开通成功 from %s to %s ' % (SourceIp, TargetIp))
            return 'sucess'
        else:
            return 'sucess'

# 删除iptables策略
def RemoveIptables(SourceIp, TargetIp):
    IptablesNumbers = commands.getoutput('iptables --line-numbers  -L FORWARD  |grep %s | grep %s | wc -l' % (SourceIp, TargetIp))
    if int(IptablesNumbers) == 0 : return
    for i in int(IptablesNumbers):
        IptablesId = commands.getoutput('iptables --line-numbers  -L FORWARD  |grep %s | grep %s' % (SourceIp, TargetIp))
        IptablesRemoveId = IptablesId.split()[0]
        os.popen('iptables -D FORWARD %s' % (IptablesRemoveId))
        log('策略删除成功 from %s to %s ' % (SourceIp, TargetIp))


def main():
    FireWallConf = open("/FireWall/conf/FireWall.conf", 'r')
    for i in FireWallConf.readlines():
        ExpiredTime = i.split()[2]
        DateNow = datetime.datetime.now()
        DateNow = DateNow.strftime('%Y%m%d')
        SourceIp = i.split()[0]
        TargetIp = i.split()[1]
        print('info:::%s,source %s, target %s' % (ExpiredTime, SourceIp, TargetIp))
        if DateNow > ExpiredTime:
            RemoveIptables(SourceIp, TargetIp)
        else:
            AddIptables(SourceIp, TargetIp)


if __name__ == '__main__':
    while 1 :
        time.sleep(300)
        main()

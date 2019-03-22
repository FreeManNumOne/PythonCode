#!/usr/bin/env python
#-*-coding:utf-8-*-
#version 0.1
#date 20181220
#mail:

import  logs
import  main
import  sys
import  datetime

def Frontend():
    HostIp=sys.argv[1]
    PackageName= sys.argv[2]
    ServiceName = PackageName.split(".")[0]
    UserName = 'root'
    PassWord='xxxx'

    for i in HostIp.split(":"):
        #print(i)
        HostIP = i
        print(HostIP,PackageName,ServiceName,UserName)
        FrontendUat=main.Release(HostIP,PackageName,ServiceName,UserName,PassWord)
        DatetimeNowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.bak')
        cmd= 'mv /data/%s  /data/backup/%s_%s'%(ServiceName,ServiceName,DatetimeNowTime)
        FrontendUat.RemoteCommandRun(cmd)
        logs.log('%s %s run success' % (HostIP, cmd))
        print('%s %s run success' % (HostIP, cmd))
        cmd2 = 'mkdir -p /data/%s'%ServiceName
        FrontendUat.RemoteCommandRun(cmd2)
        logs.log('%s %s run success' % (HostIP, cmd2))
        print ('%s %s run success' % (HostIP, cmd2))
        FrontendUat.FilesTransport()
        cmd3 = 'cd /data/%s && tar -xzvf %s && rm -rf /data/%s/%s'%(ServiceName,PackageName,ServiceName,PackageName)
        #print(cmd3)
        FrontendUat.RemoteCommandRun(cmd3)
        logs.log('%s %s run success'%(HostIP,cmd3))
        logs.log('Frontend Info:%s %s %s %s %s ' % (HostIP,PackageName,ServiceName,UserName,PassWord))
        print('%s %s run success'%(HostIP,cmd3))
    else:
        logs.log("Frontend release done")

if __name__ == '__main__':
    Frontend()

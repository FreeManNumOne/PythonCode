#!/usr/bin/env python
#-*- conding:utf-8 -*-

import  datetime
import  os

def ConfigRewrite():
    FireWallConf = open("/FireWall/conf/FireWall.conf", 'r')
    for i in FireWallConf.readlines():
        ExpiredTime = i.split()[2]
        DateNow = datetime.datetime.now()
        DateNow = DateNow.strftime('%Y%m%d')
        SourceIp = i.split()[0]
        TargetIp = i.split()[1]
        if DateNow > ExpiredTime:
            os.system("sed -i '/%s/d' /FireWall/conf/FireWall.conf"%i)
            return 'DeleteSucess'
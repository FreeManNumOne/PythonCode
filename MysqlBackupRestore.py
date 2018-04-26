#!/usr/bin/env python
# -*- coding: utf-8 -*-
#用于基库导入导出的功能

import  os
import  sys
import  commands
import  paramiko
import  MySQLdb

def MysqlBackup(Ip,MysqlUser,PassWord,DatabaseName,DatabasePort,BackupDir):
    DirExists=os.path.exists(BackupDir)
    if DirExists == True:
        #print ('%s exists'%BackupDir)
        pass
    else:
        os.mkdir(BackupDir)
        print ('%s creater dir sucess'%BackupDir)
    CheckSqlFielsExists = os.listdir(BackupDir)
    for i in CheckSqlFielsExists:
        if i == '%s.sql'%DatabaseName:
            print ('Please Delete %s/%s.sql or bakcup %s.sql'%(BackupDir,DatabaseName,DatabaseName))
            sys.exit()
    cmd = 'mysqldump -u%s -p%s -h%s %s >%s/%s.sql' % (MysqlUser,PassWord,Ip,DatabaseName,BackupDir,DatabaseName)
    print(cmd)
    k, v = commands.getstatusoutput(cmd)
    if k == 0:
        print ( 'MysqlDump  %s %s Sucess'%(Ip,DatabaseName))
    else:
        print('MysqlDump %s %s Failed'%(Ip,DatabaseName))
        sys.exit()


def RemoteBackupDatabase():
    pass

def RemoteCheckDatabase():
    pass

def UploadSql(TarGetIp,SystemUser,SystemPassword,RemoteDir,LocalDir):
    t = paramiko.Transport((TarGetIp))
    t.connect(username=SystemUser,password=SystemPassword)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(LocalDir, RemoteDir)
    t.close()

def MysqlRecovery(TarGetIp,SystemUser,SystemPassword,SshPort,MysqlUser,MysqlPassword,DatabaseName,DatabasePort,BackupDir,LocalDir):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(TarGetIp, SshPort, SystemUser, SystemPassword)
    stdin, stdout, stderr = ssh.exec_command("ls %s" % (BackupDir))
    StdoutAll=stdout.readlines()
    if len(StdoutAll) != '':
        pass
    else:
        stdin, stdout, stderr = ssh.exec_command("mkdir -p %s" % (BackupDir))
        print("%s Creater %s dir sucess"%(TarGetIp,BackupDir))
    for i in StdoutAll:
        if i == '%s.sql'%(DatabaseName):
            print('Please Delete %s  %s/%s.sql or bakcup %s.sql' % (TarGetIp,BackupDir, DatabaseName, DatabaseName))
            sys.exit()
    RemoteName='%s/%s.sql'(BackupDir,DatabaseName)
    LocalName='%s/%s.sql'(LocalDir,DatabaseName)
    UploadSql(TarGetIp,SystemUser,SystemPassword,RemoteName,LocalName)
    #stdin, stdout, stderr = ssh.exec_command("mysql -u%s -p%s %s < %s/%s.sql" % (MysqlUser,MysqlPassword,DatabaseName,BackupDir,DatabaseName))

if __name__ == "__main__":
    TarGetIP=sys.argv[1]
    SystemUser=sys.argv[2]
    SystemPassword=sys.argv[3]

    MysqlBackup('192.168.200.5','namibank','namibank123','base','3306','/opt/databasebak')
    MysqlBackup('192.168.200.5', 'namibank', 'namibank123', 'risk', '3306', '/opt/databasebak')
    MysqlBackup('192.168.200.5', 'namibank', 'namibank123', 'mall', '3306', '/opt/databasebak')
    MysqlBackup('192.168.200.5', 'namibank', 'namibank123', 'gate', '3306', '/opt/databasebak')
    MysqlRecovery(TarGetIP,SystemUser,SystemPassword,22,'namibank','base','3306','/data/databasebak')

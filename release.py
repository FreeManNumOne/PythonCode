#!/usr/bin/env python

import  sys
import  logs
import  hashlib
import  datetime
import  paramiko

class Release(object):
    def __init__(self,HostIP,PackageName,ServiceName,UserName,PassWord):
        self.HostIP = HostIP
        self.PackageName = PackageName
        self.ServiceName = ServiceName
        self.UserName = UserName
        self.PassWord = PassWord
        self.SSHPort = 22
        self.TargetDir = '/data/'
        self.PackageDir = '/data/packages/'

    #File transfer module
    def FilesTransport(self):
        t = paramiko.Transport((self.HostIP, self.SSHPort))
        print ("tttt",self.HostIP,self.SSHPort,self.UserName,self.PassWord)
        t.connect(username=self.UserName,password=self.PassWord) #,password=self.PassWord)
        sftp = paramiko.SFTPClient.from_transport(t)
        #sftp.get('/root/test.py', '/test.py')
        UploadFileName='%s%s'%(self.PackageDir,self.PackageName)
        TargetName='%s%s/%s'%(self.TargetDir,self.ServiceName,self.PackageName)
        print(UploadFileName,TargetName)
        sftp.put(UploadFileName,TargetName)
        t.close()
        logs.log('UpLoadFiles  %s to %s'%(self.PackageName, self.HostIP))
        return  'FileTransportSuccess'

    #RemoteCommand  module
    def RemoteCommandRun(self,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.HostIP,port=self.SSHPort,username=self.UserName,password=self.PassWord)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        done = stdout.readlines()
        #print(done)
        logs.log('command run done %s and result %s'%(cmd,done))
        return (done)

    #Stop target Service
    def StopService(self):
        cmd='supervisorctl  stop %s'%self.ServiceName
        StopServiceStatus=self.RemoteCommandRun(cmd)
        for i in StopServiceStatus:
            if 'ERROR' in i :
                print ('%s Service Not Running'%self.ServiceName)
                logs.log('%s Service Not Running'%self.ServiceName)
            elif 'STOP' in i:
                print ('%s Service Stop Success'%self.ServiceName)
                logs.log('%s Service Stop Success'%self.ServiceName)
            elif 'stopped' in i :
                print ('%s Service Stop Success'%self.ServiceName)
                logs.log('%s Service Stop Success'%self.ServiceName)
            #print('stop',i)

    #Check if the target file is empty
    def CheckFile(self):
        cmd="ls -lh %s%s/%s"%(self.TargetDir,self.ServiceName,self.PackageName)
        #print(cmd)
        CheckFileDone=self.RemoteCommandRun(cmd)
        #print(CheckFileDone)
        if CheckFileDone:
            logs.log('CheckFileNotEmpty %s'%cmd)
            print('CheckFileNotEmpty %s'%cmd)
            return 'CheckFileNotEmpty'
        else :
            logs.log('CheckFileEmpty %s' % cmd)
            print('CheckFileEmpty %s' % cmd)
            return 'CheckFileEmpty'

    #Target packet Backup
    def BackupService(self):
        CheckFileStatus=self.CheckFile()
        if CheckFileStatus == 'CheckFileEmpty':
            return 0
        DatetimeNowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S.bak')
        cmd='mv /data/%s/%s  /data/backup/%s.%s'%(self.ServiceName,self.PackageName,self.PackageName,DatetimeNowTime)
        self.RemoteCommandRun(cmd)
        cmd2 = 'ls -l /data/backup/%s.%s'%(self.PackageName,DatetimeNowTime)
        BackupServiceStatus=self.RemoteCommandRun(cmd2)
        #print('cmd',cmd)
        #print('cmd2',cmd2)
        #Process the \\n returned by the command
        BackupPackageName="/data/backup/%s.%s\\n']"%(self.PackageName,DatetimeNowTime)
        #print('1:',str(BackupServiceStatus).split()[-1])
        #print('2:',BackupPackageName)
        if str(BackupServiceStatus).split()[-1] == BackupPackageName:
            print('%s Backup success '%BackupPackageName)
            logs.log('%s Backup success '%BackupPackageName)
        else:
            print('%s Backup Failed'%BackupPackageName)
            logs.log('%s Backup Failed'%BackupPackageName)

    #Calculation source file md5Sum
    def SourceMd5Sum(self,filename):
        filename='%s%s'%(self.PackageDir,filename)
        with open(filename, 'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            #print(hash)
            logs.log('SourceMd5Sum %s  md5Code %s'%(filename,hash))
            return hash

    #Source and target packet check
    def PackageMd5Sum(self):
        SourceMD5=self.SourceMd5Sum(self.PackageName)
        cmd = 'md5sum %s%s/%s'%(self.TargetDir,self.ServiceName,self.PackageName)
        TargetMD5=self.RemoteCommandRun(cmd)
        if str(TargetMD5).split()[0].split("'")[1] == str(SourceMD5).strip():
            #print('SourceMd5:%s' % SourceMD5)
            #print('TargetMd5:%s' %str(TargetMD5).split()[0].split("'")[1])
            #print('Md5Sum sucesss %s'%(PackageName))
            print('Md5Sum sucesss %s SourceMd5:%s TargetMd5:%s'%(self.PackageName,SourceMD5,TargetMD5))
            logs.log('Md5Sum sucesss %s SourceMd5:%s TargetMd5:%s'%(self.PackageName,SourceMD5,TargetMD5))
        else:
            #print('SourceMd5:%s' % SourceMD5)
            #print('TargetMd5:%s' % str(TargetMD5).split()[0]).encode("UTF-8")
            #print('%s FileTransport Failed!'%(PackageName))
            print('%s FileTransport Failed! SourceMd5:%s TargetMd5:%s '%(self.PackageName,SourceMD5,TargetMD5))
            logs.log('%s FileTransport Failed! SourceMd5:%s TargetMd5:%s '%(self.PackageName,SourceMD5,TargetMD5))
            sys.exit()

    #Target service startup
    def StartService(self):
        cmd = 'supervisorctl  start %s' % ServiceName
        StartServiceStatus = self.RemoteCommandRun(cmd)
        for i in  StartServiceStatus :
            if 'ERROR' in i :
                print ('%s Service Start Failed'%self.ServiceName)
                logs.log('%s Service Start Failed'%self.ServiceName)
                sys.exit(1)
            elif 'RUNNING' in i:
                print('%s Service Start Success' % self.ServiceName)
                logs.log('%s Service Start Success' % self.ServiceName)
            elif 'started' in i :
                print('%s Service Start Success' % self.ServiceName)
                logs.log('%s Service Start Success' % self.ServiceName)
            #print('start',i)

    #Program entry
    def main(self):
        self.StopService()
        #self.BackupService()
        self.FilesTransport()
        self.PackageMd5Sum()
        self.StartService()
        print ('Info:',self.HostIP,self.ServiceName,self.PackageName,self.UserName)
        logs.log('One Release Info:%s , %s, %s, %s, %s'%(self.HostIP,self.ServiceName,self.PackageName,self.UserName,self.PassWord))


if __name__ == '__main__':
    HostIp=sys.argv[1]
    PackageName= sys.argv[2]
    ServiceName = '-'.join(PackageName.split(".")[:-1])
    UserName = 'root'
    PassWord='xxxxxxx'
    for i in HostIp.split(":"):
        #print(i)
        HostIp = i
        #print (HostIp,PackageName,ServiceName,UserName,PassWord)
        ReleaseTest=Release(HostIp,PackageName,ServiceName,UserName,PassWord)
        ReleaseTest.main()
    else:
        logs.log("release done")

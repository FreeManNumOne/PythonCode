#!/usr/bin/env python
#2018/06/11
#version  0.1

import  paramiko
import  sys
import  Passwd2



def CommandRun(Host,Package,PackageName,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=Host, port=22, username='root', password=password)
    cmd= 'md5sum /data/vnbig-%s/%s'%(Package,PackageName)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    err = stderr.read()
    ssh.close()
    print(result.split()[0])
    return result.split()[0]

def Md5Check(SourceMd5,TargetMd5Code):
    if SourceMd5 == TargetMd5Code:
         return True
    else:
         return False

def Main(FileName):
    OpenFile=open(FileName,'r')
    for i in OpenFile.readlines():
        if '#' in i:
             continue
        ip = i.split()[0]
        PackageName=i.split()[1]
        Package=PackageName.split('.')[2]
        SourceMd5Code=i.split()[2]
        print (PackageName)
        print (Package)
        password = Passwd2.prpcrypt('keys')
        password2 = password.decrypt('625787c88d24455833a44d07a47cc12b8d041a8d2b5bc1328431be020e7e456e')
        TargetMd5Code = CommandRun(ip,Package,PackageName,password2)
        Done=Md5Check(SourceMd5Code,TargetMd5Code)
        if Done is True:
            print ('check jar done')
        else:
            print ('check jar error')
        

if __name__ == "__main__":
    PackageFileName=sys.argv[1]
    Main(PackageFileName)

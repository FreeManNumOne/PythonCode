import main
import  sys

def GetLogs():
    HostIp=sys.argv[1]
    PackageName= sys.argv[2]
    ServiceName = '-'.join(PackageName.split("-")[:-1])
    UserName = 'root'
    PassWord='zzzzzz'
    for i in HostIp.split(":"):
        #print(i)
        HostIP = i
        #print(HostIP,ServiceName)
        GetLogs=main.Release(HostIP,PackageName,ServiceName,UserName,PassWord)
        GetLogs.ServiceLogsOut()

if __name__ == '__main__':
    GetLogs()
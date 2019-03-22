#!/usr/bin/env python
#auth Yong.jianzhuang
#version 0.1
#date 20181214
#mail: Yong.jianzhuang@dr-elephant.com

import  urllib2
import  json
import  requests
import  logs

class UrlCheck(object):
    def __init__(self,GetAllUrl,Data,Ip):
        self.GetAllUrl = GetAllUrl
        self.Data = Data
        self.Ip = Ip

    #Get Data
    def GetAllDone(self):
        request = urllib2.Request(self.GetAllUrl)
        request.add_header("Content-Type", "application/json")
        request.add_header("Accept", "application/json")
        request.get_method = lambda: "GET"  # "GET,POST,PUT,DELETE"
        response = urllib2.urlopen(request)
        response_txt = response.read()
        #response_header = response.info()
        return response_txt

    #DataAnalysis
    def DataAnalysis(self):
        DataAnalysisDone = json.loads(self.GetAllDone())
        DataAnalysisDone1 = dict(DataAnalysisDone.get('applications'))
        DataAnalysisDone2 = DataAnalysisDone1.get('application')
        for i in DataAnalysisDone2:
            done = i.get('instance')
            for i in done:
                print(i.get('app'))
                print(i.get('statusPageUrl'))
                if self.Data == i.get('app') and self.Ip == i.get('ipAddr'):
                    StatusPageUrl = i.get('statusPageUrl')
                    return StatusPageUrl

    #Check if the return status code is 200
    def UrlCheckCode(self,url):
        try:
            request = requests.get(url)
            httpStatusCode = request.status_code
            #print (httpStatusCode)
            return httpStatusCode
        except requests.exceptions.HTTPError as e:
            return e

    #Url Check Program entry
    def UrlCheckMain(self):
        StatusPageUrl = self.DataAnalysis()
        UrlCheckCodeDone= self.UrlCheckCode(StatusPageUrl)
        try :
            if UrlCheckCodeDone == 200 :
                print('status--->',StatusPageUrl,UrlCheckCodeDone)
                return  '%sUrlCheckSuccess'%(self.Data)
            else:
                print('no 200 code')
                print(StatusPageUrl)
                return '%sUrlCheckFailed'%(self.Data)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    UrlCheck1 = UrlCheck('http://uat-eureka1.dr-elephant.net:8861/eureka/apps','DRUG')
    UrlCheck1.UrlCheckMain()

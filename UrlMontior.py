#!/usr/bin/env python
#auth Yong.jianzhuang
#version 0.1
#date 20190220
#mail: Yong.jianzhuang@dr-elephant.com

import  urllib2
import  json
import  requests
import  time
import  mail

class UrlCheck(object):
    def __init__(self,GetAllUrl):
        self.GetAllUrl = GetAllUrl
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
        StatusPageUrlAll = []
        for i in DataAnalysisDone2:
            done = i.get('instance')
            for i in done:
                #print(i.get('app'))
                AppName = i.get('app')
                AppCheckUrl = i.get('statusPageUrl')
                #print('%s %s'%(AppName,AppCheckUrl))
                StatusPageUrl =(('%s %s')%(AppName,AppCheckUrl))
                #print(StatusPageUrl)
                StatusPageUrlAll.append(StatusPageUrl)
        return StatusPageUrlAll

    #Check if the return status code is 200
    def UrlCheckCode(self,url):
        if 'gateway.elephantdr.com' in url:
            for i in ['http://192.168.9.1:8871/info','http://192.168.9.2:8871/info']:
                try:
                    request = requests.get(i)
                    httpStatusCode = request.status_code
                    # print (httpStatusCode)
                    return httpStatusCode
                except requests.exceptions.HTTPError as e:
                    return e
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
        print(StatusPageUrl)
        time.sleep(500)
        StatusPageUrl2 = self.DataAnalysis()
        ret = set(StatusPageUrl) ^ set(StatusPageUrl2)
        if len(ret) ==0:
            pass
        else:
            for i in ret:
                print ('ret %i',i)
                msg = ('%s stop running' % i)
                mail.Sendmail(msg)
        for i in StatusPageUrl2:
            if "PINGPLUS" == i.split()[0].strip():
                print('pingplus', i)
                continue
            UrlCheckCodeDone= self.UrlCheckCode(i.split()[1])
            try :
                if UrlCheckCodeDone == 200 :
                    print('status--->',i,UrlCheckCodeDone)
                    #return  '%sUrlCheckSuccess'
                else:
                    print('%s no 200 code'%(i))
                    msg = ('%s stop running'%i)
                    mail.Sendmail(msg)
                    #return '%sUrlCheckFailed'%(i)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    while True:
       InsUrl='http://192.168.9.1:8861/eureka/apps'
       request = requests.get(InsUrl)
       httpStatusCode = request.status_code
       if httpStatusCode == 200:
           pass
           # return  '%sUrlCheckSuccess'
       else:
           print(' no 200 code')
           msg = ('%s stop running'%(InsUrl))
           mail.Sendmail(msg)
           break
       # print (httpStatusCode)
       UrlCheck1 = UrlCheck(InsUrl)
       UrlCheck1.UrlCheckMain()

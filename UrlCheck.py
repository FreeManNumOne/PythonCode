# ! /usr/bin/env python
# coding=utf-8
import sys
import requests


def getHttpStatusCode(url):
    try:
        request = requests.get(url)
        httpStatusCode = request.status_code
        # print httpStatusCode
        return httpStatusCode
    except requests.exceptions.HTTPError as e:
        return e

if __name__ == "__main__":
    with open('UrlCheckList.conf', 'r') as f:
        for line in f.readlines():
            try:
                status = getHttpStatusCode(line.strip())
                if status == 200:
                    print('status--->', status)
                    print (line)
                else:
                    print ('no 200 code')
                    print (line)
            except Exception as e:
                print (e)

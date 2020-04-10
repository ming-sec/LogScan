#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Python 3
# By Ming

import requests
import time
import sys
#python 3.7 解决https报错
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
'''
低于 python 3.7  版本
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
'''

path1 = ['/Application/','/application/','/App/','/app/','/Runtime/','/runtime/','/Run/','/run/','/Temp/','/temp/']

path2_big = ['Runtime/','Run/','Logs/','Log/']
path2_small = ['runtime/','run/','logs/','log/']

path3_big = ['Home/','Logs/','Log/','User/','Index/','Admin/','User/','Common/']
path3_small = ['home/','logs/','log/','user/','index/','admin/','user/','common/']

path4_big = ['Home/','Index/']
path4_small = ['home/','index/']

path5 = []


now_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
year1 = now_time.split(' ')[0].replace('-','_')[2:]         # 20_03_23
year2 = now_time.split(' ')[0].split('-')[0] + now_time.split(' ')[0].split('-')[1]  # 202003

day = year1.split('_')[2]   # 23
year = year1.split('_')[0]  # 20
month = year1.split('_')[1] # 03

res = []

log1 = year1 + ".log";  #  20_03_22.log
log2 = day + ".log";  # 23.log

path3_big.append(year2)
path3_small.append(year2)

path3_big.append(log1)
path3_small.append(log1)

path4_big.append(log1)
path4_small.append(log1)

path4_big.append(log2)
path4_small.append(log2)

path5.append(log1)


def GetResponse(url):
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    try:
        req = requests.get(url=url,headers=headers,timeout=1)
        code = req.status_code
        return code
    except Exception as e:
        return None

def getdate(year,month,icon):
    list1 = []  # 年
    list2 = []  # 月
    list3 = []  # 日
    list1.append(str(year))
    if int(month) < 3:
        list2.append('01')
        list2.append('02')
    elif int(month) >= 3:
        for i in range(int(month)-3,int(month)):
            temp = str(i + 1)
            if len(temp) == 2:
                list2.append(temp)
            else:
                list2.append("0" + temp) 
    for j in range(30):
        temp2 = str(j + 1)
        if len(temp2) == 2:
            list3.append(temp2)
        else:
            list3.append("0" + temp2) 
    date = []
    date2 = []
    for a in list1:
        for b in list2:
            for c in list3:
                last1 = a + '_' + b + '_' + c + '.log'
                last2 = '20' + a + b + '/' + c + '.log'
                date.append(last1)
                date2.append(last2)
    if icon == 1:
        return date
    elif icon == 2:
        return date2



def scan_more(result,year):
    if len(result)==0:
        print('No Logs find!')
        return None
    else:
        print("\n[+]Scan more Log start!====================" + "\n")
        print("[+]All Result Show:   ")
        today = result[0] # http://www.qiantai.com/Application/Runtime/Logs/16_09_09.log
        length = len(today.split('/')[-1])
        if length == 12:
            url = today[:-12]
            date = getdate(year,month,1)
            days = len(date)
            for key in date:
                url2 = url + key
                code6 = GetResponse(url2)
                if code6 == 200:
                        position = date.index(key) + 1
                        print_res(url2,position,days)
        elif length == 6:    #http://www.qiantai.com/runtime/logs/202002/09.log
            url = today[:-13]
            date = getdate(year,month,2)
            days = len(date)
            for key in date:
                url2 = url + key
                code6 = GetResponse(url2)
                if code6 == 200:
                        position = date.index(key) + 1
                        print_res(url2,position,days)

def main(url):
    print("[+]Start!====================" + "\n")
    for a in path1:
        temp = url + a
        code = GetResponse(temp)
        if code == 403:
            if a.istitle() == True:
                for b in path2_big:
                    temp2 = temp + b
                    code2 = GetResponse(temp2)
                    if code2 == 403:
                        for c in path3_big:
                            temp3 =  temp2 + c
                            code3 = GetResponse(temp3)
                            if code3 == 200:
                                res.append(temp3)
                            elif code3 == 403:
                                for d in path4_big:
                                    temp4 = temp3 + d
                                    code4 = GetResponse(temp4)
                                    if code4 == 200:
                                        res.append(temp4)
                                    elif code4 == 403:
                                        for e in path5:
                                            temp5 = temp4 + e
                                            code5 = GetResponse(temp5)
                                            if code5 == 200:
                                                res.append(temp5)
            else:
                for b in path2_small:
                    temp2 = temp + b
                    code2 = GetResponse(temp2)
                    if code2 == 403:
                        for c in path3_small:
                            temp3 =  temp2 + c
                            code3 = GetResponse(temp3)
                            if code3 == 200:
                                res.append(temp3)
                            elif code3 == 403:
                                for d in path4_small:
                                    temp4 = temp3 + d
                                    code4 = GetResponse(temp4)
                                    if code4 == 200:
                                        res.append(temp4)
                                    elif code4 == 403:
                                        for e in path5:
                                            temp5 = temp4 + e
                                            code5 = GetResponse(temp5)
                                            if code5 == 200:
                                                res.append(temp5)
    res3 = []
    result = []
    for i in res:
        print('Find: ' + i)
        j = i.lower()
        if j not in res3:
            res3.append(j)
            result.append(i)
    result_res = scan_more(result,year)
    print("Finished======================!")


def print_res(url,position,days):
    output = sys.stdout  
    output.write(' ' * 100 + '\r')
    output.flush()
    print('Success: ' + url)
    output.write('Complete  ----->: %s/%s\r' %(position,days) )
    output.flush()

if __name__ == '__main__':
    print("[+]Usage: scan.py http://www.baidu.com")
    if sys.argv[1] != '':
        url = sys.argv[1]
        main(url)
    else:
        sys.exit()

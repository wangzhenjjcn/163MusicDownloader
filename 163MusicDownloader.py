#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,time,datetime,os,requests
import json
# import rsa
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
# import base64
# from PIL import Image
# from random import random
data_file=open("./tmp/data.csv","a",encoding='utf-8')
songList={}
try:
    import cookielib
    print(f"python2.")
except:
    import http.cookiejar as cookielib
    print(f"python3.")
webSession = requests.session()
webSession.cookies = cookielib.LWPCookieJar(filename = "cookie.txt")
download_path="./download/"
defaulturl = "http://music.sonimei.cn/"

defaultHeader = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'dnt': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
        'cache-control': "no-cache"
        }

def searchMusicByIdAndProvider(mid,provider):
    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'dnt': "1",
        'accept-encoding': "gzip, deflate",
        'x-requested-with': "XMLHttpRequest",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
        'cache-control': "no-cache",
        'accept': "application/json, text/javascript, */*; q=0.01",
    }
    ptype=provider
    if(ptype == None):
        ptype="netease"
    postData = { 
        "input": mid,
        "filter": "id",
        "type": ptype,
        "page": 1,
        }
    responseRes = webSession.post(defaulturl, data = postData, headers = headers,verify=False )
    webSession.cookies.save()
    print(f"statusCode = {responseRes.status_code}"+":"+defaulturl)
    #print(f"text = {responseRes.text.encode('utf-8').decode('unicode_escape')}")
    r_file=open("./tmp/"+str(mid)+"-"+str(ptype),"w",encoding="utf-8")
    try:
        data=json.loads(responseRes.text)
        r_file.write(str(data))
        r_file.flush()
    except:
        responseRes.text
    finally:
        r_file.close()
    return responseRes.text

def downloadMusic(filename,url):
    _filename=filename.replace(",","+").replace(" ","")
    c = "powershell -Command \"Invoke-WebRequest %s -OutFile %s\"" % (url,download_path+_filename)
    print(c)
    os.system(c)

def downloadMusicFrom163ById(mid):
    data=searchMusicByIdAndProvider(mid,"netease")
    data=json.loads(data)
    filename=data['data'][0]['author']+"-"+data['data'][0]['title']+".mp3"
    filename=filename.replace(",","+")
    url=data['data'][0]['url']
    downloadMusic(filename,url)

if __name__ == "__main__":
    # webSession.cookies.load()
    # print(webSession.cookies)
    mid=input()
    mid=mid.upper()
    downloadMusicFrom163ById(mid)
    
data_file.close()
if data_file:
    data_file.close()
# -*- coding:UTF-8 -*-
#!/usr/bin/python2
#this is for "沈非欢 的收藏"

import requests
import threading
from bs4 import BeautifulSoup
import re
import time

class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.144.1.10:8080',
            "https": 'https://10.144.1.10:8080'}
        self.base_url = 'https://www.zhihu.com/collection/40258902?page=1'
        self.naviUrl = 'https://www.zhihu.com/collection/40258902?page=1'
        self.prefixUrl = 'https://www.zhihu.com'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://www.meizitu.com'
}

setting = NetWorkSetting()
"""
Description    : 将网页图片保存本地
@param imgUrl  : 待保存图片URL
@param imgName : 待保存图片名称
@return 无
"""
def saveImage( imgUrl,imgName ="default.jpg" ):
    response = requests.get(imgUrl, headers=setting.myHeaders, proxies=setting.proxy)
    #response = requests.get(imgUrl, stream=True, headers=setting.myHeaders, proxies=setting.proxy)
    image = response.content
    DstDir="D:\\persion\\picture\\downimg\\"
    print("保存文件"+DstDir+imgName+"\n")
    try:
        with open(DstDir+imgName,"wb") as jpg:
            jpg.write( image)
        return
    except IOError:
        print("IO Error\n")
        return
    finally:
        jpg.close



"""
Description    : 将网页保存本地
@param imgUrl  : 待保存html URL
@param imgName : 待保存html名称
@return 无
"""
def saveHtml( htmlUrl,imgName ="default.html" ):
    response = requests.get(htmlUrl, headers=setting.myHeaders, proxies=setting.proxy)
    DstDir="D:\\zhihu\\1\\"
    print("保存文件"+DstDir+imgName+"\n")
    f = open(DstDir+imgName, 'w+')
    f.write(response.content)
    f.flush()
    f.close()

"""
Description    : 开启多线程执行下载任务
@param filelist:待下载图片URL列表
@return 无
"""


def downTopicViaMutiThread( filelist ):
    print "2, enter downImageViaMutiThread"
    task_threads=[]  #存储线程
    count = 1
    for file in filelist:
        print file
        filename = file.replace("/","-")
        if 'com-' in filename:
            p = re.compile(r'com-')
        print(filename)
        filename = p.split(filename)[1]
        filename += ".html"
        t = threading.Thread(target=saveHtml,args=(file,filename))
        count += 1
        task_threads.append(t)
    for task in task_threads:
        task.start()
    for task in task_threads:
        task.join()

"""
Description    : 获取图片地址
@param pageUrl : 网页URL
@return : 图片地址列表
"""

def getfilelist(pageUrl):
    print "1, enter getfilelist"
    web = requests.get(pageUrl, headers=setting.myHeaders, proxies=setting.proxy)
    soup = BeautifulSoup(web.text)
    filelist=[]
    #   for photo in soup.find_all('img',{'class':'scrollLoading'}):
    for topic in soup.find_all('a'):
        if topic.has_attr("target") and topic.get("target") == "_blank":
            if topic.has_attr("href") and topic.get("href").find("question") != -1 and topic.get("href").find("answer") == -1:
                filelist.append(setting.prefixUrl + topic.get('href'))
    print "1, leave getfilelist"
    return filelist

def getUrlListInPage(webUrl):
    #https://www.zhihu.com/collection/40258902?page=1
    weblist=[]
    print "0, enter getweblist"
    targeturl = webUrl
    index = 0
    temp = 1
    web = requests.get(targeturl, headers=setting.myHeaders, proxies=setting.proxy)
    if web.status_code == 200:
        soup = BeautifulSoup(web.content)
        for pageNumber in soup.find_all('a'):
            if pageNumber.has_attr("href") and pageNumber.get("href").find("?page=") != -1:
                temp = pageNumber.get("href")[-1:]
                if temp > index:
                    index = temp

    count = 1
    urlPrefix = webUrl[:-1]
    tempurl = ""
    index = int(index)
    while count <= index:
        tempurl = urlPrefix + str(count)
        #print isinstance(zhihu.py, int)
        weblist.append(tempurl)
        count += 1

    print "0, leave getweblist"
    f = open("page.txt",'w+')
    for item in weblist:
        f.write(item)
        f.write('\n')
    f.close()
    return weblist

if __name__ == "__main__":
    webUrl = 'https://www.zhihu.com/collection/40258902?page=1'
    urls = getUrlListInPage(webUrl)
    print urls
    for url in urls:
        #topicList stand for topics in one page
        topicList=getfilelist(url)
        #use muti thread to capture the topics at the same time
        downTopicViaMutiThread(topicList)
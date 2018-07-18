#!/usr/bin/python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import socket
import re
socket.setdefaulttimeout(50)

#处理图片方法

def getImg(url, i, all):
    urla = url
    req = urllib2.Request(urla)
    req.add_header('Referer','//www.tuku.cn/')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html,'lxml')
    imgtag = soup.find_all('img')
    x = 0
    for link in imgtag:
        if(link.get('src') and re.match('.*\/\/.*', link.get('src'))):
            url = 'https:'+link.get('src')
            print(url+'-----%s' % x)
            urllib.urlretrieve(link.get('src'), 'img/%s-%s.jpg' % (i,x))
            x+=1
    print('====处理完第%s页了,还剩%s页====' % (i, (all-i)))

#这里是组装url
def listHtml(url, num):
    reurl = ''
    i = 1
    while(i <= num):
        reurl = url+'/page%s.aspx' % i

        getImg(reurl, i, num)
        i+=1;

#主方法
def main():
    myurl = 'http://www.tuku.cn/bizhi'
    listHtml(myurl, 86)

main()

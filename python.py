#!/usr/bin/python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import socket
import re
import time
import sys
socket.setdefaulttimeout(50)

a = 'http://www.tuku.cn/bizhi/'
b = 'http://www.tuku.cn/'
while(a == None or b == None):
    a = raw_input('请输入网址：')
    b = raw_input('请输入host：')

class GetImg:
    allnum = 1
    def __init__(self, url, host):
        self.url = url
        self.host = host

    #进度条
    def cbk(self, a, b, c):
        per = 100.0 * a * b / c
        if(per > 100):
            per = 100
        print('%2f%%' % per)

    #处理图片方法
    def getImg(self, url, i):
        print(url,i)
        urla = url
        html = self.urlRequest(url)
        if(html == None):
            return html
        soup = BeautifulSoup(html,'lxml')
        #取分页
        page_num_html = soup.find_all('div', attrs={"class": "fenye"})
        pattern = re.compile("分(\d+)页")
        if(len(page_num_html) > 0):
            result = pattern.findall(str(page_num_html[0]))
            if(result):
                self.allnum = int(result[0])
                print('当前页数是%s,总页数是%s页！！！！' % (i, self.allnum))
        else:
            self.allnum = int(1)
        imgtag = soup.find('div', attrs={"class":"box"}).find_all('img')
        x = 0
        for img in imgtag:
            #找到父级 的链接
            href = img.parent.get("href")
            if(href):
                if(re.match('.*\/\/.*', href) == None):
                    if(re.match('.*bizhi.*', href) == None):
                        href = self.url+href
                    else:
                        href = self.host+href
                self.getImg(href, i)
            else:
                print('我下载图片了%s' % img.get('src') )
                html = self.saveImg(i, img.get('src'))
        #for link in imgtag:
        #print('====处理完第%s页了,还剩%s页====' % (i, (all-i)))

    #save img
    def saveImg(self, i, src):
        redata = True
        if(src and re.match('.*\/\/.*', src)):
            try:
                url = src
                r = urllib2.Request(url)
                r.add_header('Referer', self.host)
                r.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
                res = urllib2.urlopen(r, data=None, timeout=10)
                nowt = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
                fw = open('img/%s-%s.jpg' % (i,nowt),'wb')
                fw.write(res.read())
                fw.close()
                i+= 1
            except Exception,e:
                nowt = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
                self.fwriteM('imglog', '文件下载失败', '%s-%s' % (i, nowt))
                i+= 1
                redata = None
        # return redata
    #这里是组装url
    def listHtml(self, url):
        reurl = ''
        i = 1
        while(i <= self.allnum):
            reurl = url+'/page%s.aspx' % i
            result = self.getImg(reurl, i)
            if(result):
                i+=1
                continue


    #写文件记录
    def fwriteM(self, filename, content, num):
        with open(filename,'a') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据
            nowt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write('记录问题%s--%s--{%s}完成！\r\n' % (nowt, content, num))
        f.close()

    #封装取数据
    def urlRequest(self, url):
        try:
            req = urllib2.Request(url)
            req.add_header('Referer', self.host)
            req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
            html = urllib2.urlopen(req).read()
        except Exception,e:
            html = None
        return html

    #主方法
    def main(self):
        self.listHtml(self.url)


getImg = GetImg(a, b)
getImg.main()

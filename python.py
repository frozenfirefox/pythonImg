#!/usr/bin/python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import socket
import re
import time
socket.setdefaulttimeout(50)

#进度条
def cbk(a, b, c):
    per = 100.0 * a * b / c
    if(per > 100):
        per = 100
    print('%2f%%' % per)

#处理图片方法
def getImg(url, i, all, host):
    urla = url
    req = urllib2.Request(urla)
    req.add_header('Referer', host)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html,'lxml')
    imgtag = soup.find_all('img')
    x = 0
    for link in imgtag:
        if(link.get('src') and re.match('.*\/\/.*', link.get('src'))):
            try:
                url = link.get('src')
                r = urllib2.Request(url)
                r.add_header('Referer', host)
                r.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
                res = urllib2.urlopen(r, data=None, timeout=3)
                fw = open('img/%s-%s.jpg' % (i,x),'wb')
                fw.write(res.read())
                fw.close()
                print(url+'-----%s---第%s页' % (x, i))
                #     f.fwrite(res.read())
                # print(url+'-----%s' % x)
                # try:
                #     urllib.urlretrieve(link.get('src'), 'img/%s-%s.jpg' % (i,x), cbk)
                # except Exception,e:
                #      print 'Network conditions is not good.Reloading.'
                x+=1
            except Exception,e:
                x+=1
                fwriteM('imglog', '文件下载失败', '%s-%s' % (i, x))
                continue
    print('====处理完第%s页了,还剩%s页====' % (i, (all-i)))

#这里是组装url
def listHtml(url, num, host):
    reurl = ''
    i = 1
    while(i <= num):
        reurl = url+'/page%s.aspx' % i

        getImg(reurl, i, num, host)
        i+=1;

#写文件记录
def fwriteM(filename, content, num):
    with open(filename,'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据
        nowt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write('记录问题%s--%s--{%s}完成！\r\n' % (nowt, content, num))
    f.close()

#主方法
def main():
    myurl = 'http://www.tuku.cn/bizhi'
    host = '//www.tuku.cn/'
    listHtml(myurl, 86, host)

main()


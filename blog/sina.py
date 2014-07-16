#!/usr/bin/python
#coding: gb2312
#author: jindongh@gmail.com
#description: update sina blog to redirect to a new blog

import re
import urllib2
from xmlrpclib import ServerProxy
from HTMLParser import HTMLParser

BLOG_USER="hankjin@sina.com"
BLOG_PASSWORD="mysecret"
BLOG_PAGES=10

APIURL='http://upload.move.blog.sina.com.cn/blog_rebuild/blog/xmlrpc.php'

def getCite(html):
    link="<a href='http://www.hankjohn.net/weblog/'><h3>查看原文</h3></a>"
    link=link.decode('gb2312')
    return link+"<br/>"+html+"<br/>"+link
def getList():
    result=[]
    #total pages to download
    for i in range(1,BLOG_PAGES):
        url='http://blog.sina.com.cn/s/articlelist_1347362010_0_%d.html' %i
        raw = urllib2.urlopen(url).read()
        items = re.findall('(http://blog.sina.com.cn/s/blog_[^"]*)"', raw)
        for item in items:
            result.append(item)
    return result
def editItem(tid):
    server = ServerProxy(APIURL)
    ret = server.metaWeblog.getPost(tid, BLOG_USER, BLOG_PASSWORD)
    newItem={'title':ret['title']}
    newItem['description'] = getCite(ret['description'])
    return server.metaWeblog.editPost(tid, BLOG_USER, BLOG_PASSWORD, newItem, True)

if __name__=='__main__':
    result = getList()
    for item in result:
        ret = re.findall('http://blog.sina.com.cn/s/blog_([^.]*).html', item)
        bid=ret[0]
        ret = editItem(bid)
        print 'edit %s result' % bid, ret


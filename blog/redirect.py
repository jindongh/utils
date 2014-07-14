#!/usr/bin/python
#coding: gb2312
import urllib2
import re
import sys
import os
from xmlrpclib import ServerProxy
URL='http://os.blog.163.com/api/xmlrpc/metaweblog/'
server = ServerProxy(URL)
BLOG_ID='hankjin'
BLOG_USER="hankjin@163.com"
BLOG_PASSWORD="mysecret"

def editPost(id):
    url='http://%s.blog.163.com/blog/static/%s' % (BLOG_ID, id)
    raw=urllib2.urlopen(url).read()
    bids=re.findall("id:'(.*)'", raw)
    if not 1 == len(bids):
        print 'access url %s found %d' % (url, len(bids))
        return False
    bid=bids[0]
    pubdates=re.findall('"blogsep">20([0-9]*)-([0-9]*)-([0-9]*)', raw)
    if not 1 == len(pubdates):
        print 'access url % found %d date' % (url, len(pubdates))
        return False
    year,mon,day='20%s' % pubdates[0][0],pubdates[0][1],pubdates[0][2]
    try:
        ret = server.metaWeblog.getPost(bid, BLOG_USER, BLOG_PASSWORD)
        description = ret['description'].encode('gb2312')
        if not 0 == len(re.findall('hankjohn', description)):
            print 'access url %s found hankjohn' % url
            return False
        newItem={'title':ret['title']}
        if len(description) > 128:
            description = description[:len(description)/2]
        link="<a href='http://www.hankjohn.net/weblog/%s/%s/%s/%s/'><h2>查看全文</h2></a>" % (year,mon,day,id)
        newItem['description'] = (link + "<br/>" + description + "<br/>" + link).decode('gb2312')
        wret = server.metaWeblog.editPost(bid, BLOG_USER, BLOG_PASSWORD, newItem, True)
        print newItem,wret
    except Exception as ex:
        print "hank Exception", ex
        return False
    return True


if __name__ == '__main__':
    print editPost('3373193720146146049118')
    #sys.exit(1)
    for item in os.listdir('data'):
        print editPost(item.strip())

#!/usr/bin/python
#coding: utf-8
#@author: jindongh@gmail.com
#@date: 2014-06-18
#@note: download blog data from blog.sina.com
import os
import sys
import re
import json
import urllib
import urllib2

class Blog:
    def __init__(self):
        pass
    def to_json(self):
        return json.dumps({
            'id':self.id,
            'url':self.url,
            'title':self.title.decode('gbk'),
            'pubDate':self.pubDate.decode('gbk'),
            'category':self.category.decode('gbk'),
            'description':self.content.decode('gbk')
            }, indent=4)

class Page:
    def __init__(self):
        self.nextUrl=''
        self.blog=Blog()
        pass

    def parse(self, raw, url):
        self.blog.id=os.path.basename(os.path.dirname(url))
        self.blog.url=url
        titles=re.findall('<span class="tcnt">([^<]*)</span>', raw)
        if not 1 == len(titles):
            oops('%d title found in url %s' % (len(titles),url))
        self.blog.title=titles[0]
        pubDates=re.findall(' <span class="blogsep">([^<]*)</span>', raw)
        if not 1 == len(pubDates):
            oops('%d pubDate found in url %s' % (len(pubDates), url))
        self.blog.pubDate=pubDates[0]
        pat=re.compile('<div class="bct fc05 fc11 nbw-blog ztag">(.*)<div class="nbw-blog-end">', re.DOTALL)
        contents=pat.findall(raw)
        if not 1 == len(contents):
            oops('%d content found in url %s' % (len(contents), url))
        self.blog.content=contents[0].strip()[:-6]
        categorys=re.findall('<a class="fc03 m2a" href=.*>(.*)</a>', raw)
        if not 1 == len(categorys):
            oops('%d category found in url %s' % (len(categorys), url))
        self.blog.category=categorys[0]
        return True

    def save(self, blog):
        if os.path.exists('data'):
            if not os.path.isdir('data'):
                return False
        else:
            os.path.mkdir('data')
        fp = open('data/%s' % blog.id, 'w')
        fp.write(blog.to_json())
        return True

    def hasNext(self):
        return 0 != len(self.nextUrl)

    def getNext(self):
        return self.nextUrl

def oops(msg):
    sys.stderr.write(msg)
    sys.stderr.write('\n')
    sys.exit(1)

def getUrls():
    return open('163.list').readlines()

def getPage(url):
    page = Page()
    while True:
        try:
            raw=urllib2.urlopen(url).read()
            break
        except:
            sys.stderr.write('retry %s\n' % url)
    if not page.parse(raw, url):
        oops('fail parse %s' % url)
    return page

def main():
    urls=getUrls()
    for url in urls:
        page = getPage(url.strip())
        if not page.save(page.blog):
            oops('failed save %s' % url)
        sys.stdout.write('succeed %s\n' % url)

if __name__=='__main__':
    main()

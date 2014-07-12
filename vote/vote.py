#!/usr/bin/python
import urllib2
import time
import json
import urllib

def ocr(fname):
    return 'code'
def vote(proxy_url, fp):
    proxy=urllib2.ProxyHandler({'http': proxy_url})
    opener=urllib2.build_opener(proxy)
    #urllib2.install_opener(opener)
    timestamp=int(time.time()*1000)
    imgurl='http://59.175.145.35/shuhua/getcode.php'
    voteurl='http://59.175.145.35/shuhua/view.php?sid=1&1[]=660&act=vote2&tid2=1'
    while True:
        try:
            resp=urllib2.urlopen(imgurl, timeout=10).read()
            open('ocr.jpg','w').write(resp)
            print 'get code'
            code=ocr('ocr.jpg')
            resp=urllib2.urlopen(voteurl, urllib.urlencode({'yzma': code}), timeout=10).read()
            print resp
            break
        except Exception as e:
            print '%s -1 %s' % (proxy_url, e)
            break

if __name__=='__main__':
    addrs=open('data/proxy.all').readlines()
    fp=open('available.proxy','w')
    for addr in addrs:
        vote(addr.strip(), fp)
        break
    fp.close()

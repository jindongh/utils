#!/usr/bin/python
import urllib
import sys
import re
import urllib2
class ProxyPages:
    def __init__(self, urls, fname, pat):
        self.fname='data/%s' % fname
        self.urls=urls
        self.pat=pat
        self.need_test=False
    def get_proxys(self):
        fp=open(self.fname, 'w')
        for url in self.urls:
            res=self.get_proxy(url)
            for proxy in res:
                fp.write('%s\n' % proxy)
        fp.close()
        return self.fname
    def get_proxy(self, url):
        result=[]
        try:
            res=urllib.urlopen(url).read()
            addrs=re.findall(self.pat, res)
        except:
            return result
        for addr in addrs:
            if len(addr)==2:
                proxy='http://%s:%s/' % (addr[0], addr[1])
            else:
                proxy='http://%s/' % (addr)
            if self.need_test and not self.test_proxy(proxy):
                print 'Bad Proxy %s' %  proxy
            else:
                result.append(proxy)
        return result
    def test_proxy(self,proxy_url):
        proxy=urllib2.ProxyHandler({'http': proxy_url})
        opener=urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        url='http://m.baidu.com/'
        try:
            resp=urllib2.urlopen(url, timeout=3).read()
            if '<?xml'==resp[:5]:
                return True
            else:
                return False
        except Exception as e:
            print '%s %s' % (proxy_url, e)
            return False

class ProxyPachongOrg(ProxyPages):
    def __init__(self):
        topurl='http://pachong.org'
        res=urllib.urlopen(topurl).read()
        country=['%s%s' % (topurl,item) for item in re.findall('a href="(/area/short/name/[\w]+.html)',res)]
        res=urllib.urlopen('%s/area/short/name/cn.html' % topurl).read()
        city=['%s%s' % (topurl, item) for item in re.findall('a href="(/area/city/name/[\w]+.html)',res)]
        urls=city+country+[
                    #'http://pachong.org',
                    #'http://pachong.org/transparent.html',
                    #'http://pachong.org/anonymous.html',
                    #'http://pachong.org/area/city/name/%E5%B9%BF%E5%B7%9E.html',
                ]
        ProxyPages.__init__(self,
                urls=urls,
                fname='proxy.pc',
                pat='<td>([0-9.]+)</td>\n[ ]+<td>([0-9]+)</td>')
class ProxyList(ProxyPages):
    def __init__(self):
        ProxyPages.__init__(self,
                urls=['http://free-proxy-list.net/',
                    ],
                fname='proxy.net',
                pat='<tr><td>([0-9.]+)</td><td>([0-9]+)</td>')

class Proxy360(ProxyPages):
    def __init__(self):
        ProxyPages.__init__(self,
                urls=[
                    'http://www.proxy360.cn/default.aspx',
                    ],
                fname='proxy.360',
                pat='width:140px;">\r\n[ ]+(.*)\r\n.*</span>\r\n[ ]+<span[ \w=":;>]+\r\n[ ]+(\d+)')
class US618Proxy(ProxyPages):
    def __init__(self):
        ProxyPages.__init__(self,
                urls=[
                    'http://0618.us/post/1525/',
                    ],
                fname='proxy.us',
                pat='<br/>([\d.:]+)')
class RUProxy(ProxyPages):
    def __init__(self):
        ProxyPages.__init__(self,
                urls=[
                    'http://proxy.com.ru/list_%d.html' % i for i in range(1,9)
                    ],
                fname='proxy.ru',
                pat='<tr><b><td>[\d]+</td><td>([\d\.]+)</td><td>([\d]+)')
class CNProxy(ProxyPages):
    def __init__(self):
        ProxyPages.__init__(self,
                urls=[
                    'http://cnproxy.com/proxy%d.html' % i for i in range(1,11)
                    ],
                fname='proxy.cn',
                pat='')
    def get_proxy(self,url):
        res=urllib.urlopen(url).read()
        addrs=re.findall('<tr><td>(.*)<SCRIPT.*:"\+(.+)\)<',res)
        result=[]
        chdict={'v':3,'m':4,'a':2,'l':9,'q':0,'b':5,'i':7,'w':6,'r':8,'c':1}
        for addr in addrs:
            ip=addr[0]
            port=0
            for ch in addr[1]:
                if ch in chdict:
                    port+=chdict[ch]
                elif ch=='+':
                    port*=10
                elif ch==')':
                    break
                else:
                    print ch
                    sys.exit(1)
            result.append('http://%s:%d/' % (ip, port))
        return result

if __name__=='__main__':
    proxys=[
            ProxyPachongOrg(),
            ProxyList(),
            Proxy360(),
            US618Proxy(),
            CNProxy(),
            RUProxy(),
            ]
    for proxy in proxys:
        print proxy.get_proxys()

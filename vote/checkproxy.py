#!/bin/python

import urllib2
import sys


def req(proxy_url, url):
    proxy=urllib2.ProxyHandler({'https': proxy_url})
    opener=urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    try:
        urllib2.urlopen(url, timeout=3).read()
        return True
    except:
        return False

if __name__=='__main__':
    for proxy in sys.stdin.readlines():
        if req(proxy, 'https://www.baidu.com/'):
            print proxy


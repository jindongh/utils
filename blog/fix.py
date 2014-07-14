#!/usr/bin/python
#coding: utf-8
#description: change from remote picture to local
import os
import re
raw=open('163.xml').readlines()
fp=open('163.new.xml', 'w')
for line in raw:
    for ip in ['126','163']:
        for net in ['com', 'net']:
            for pic in ['jpg', 'png', 'bmp', 'gif']:
                ret = re.findall('"(http://[^"]*%s.%s/[^"]*.%s)"' % (ip, net, pic), line)
                for item in ret:
                    raw=urllib2.urlopen(item).read()
                    if not os.path.isdir('img'):
                        os.mkdir('img')
                    open('img/%s' % os.path.basename(item), 'w').write(raw)
                    print item
                    line=re.sub(item, '/static/163/%s' % os.path.basename(item), line)
    fp.write(line)


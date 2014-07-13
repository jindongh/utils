#!/usr/bin/python
#coding: utf-8
#@author: jindongh@gmail.com
#@date: 2014-06-24
#@note: generate rss with json
import os
import sys
import re
import json
import urllib
import urllib2
import xml.dom.minidom as minidom

def getBlogs():
    blogs=[]
    ids=os.listdir('data')
    for id in ids:
        blog=json.load(open('data/%s' % id))
        blogs.append(blog)
    return blogs

def generateRSS(blogs):
    impl=minidom.getDOMImplementation()
    dom=impl.createDocument(None, 'rss', None)
    root=dom.documentElement
    channel=dom.createElement('channel')
    root.appendChild(channel)
    for blog in blogs:
        item=dom.createElement('item')
        channel.appendChild(item)
        #title
        title=dom.createElement('title')
        item.appendChild(title)
        value=dom.createCDATASection(blog['title'].encode('utf-8'))
        title.appendChild(value)
        #category
        category=dom.createElement('category')
        item.appendChild(category)
        value=dom.createTextNode(blog['category'].encode('utf-8'))
        category.appendChild(value)
        #link
        link=dom.createElement('link')
        item.appendChild(link)
        value=dom.createTextNode(blog['url'].encode('utf-8'))
        link.appendChild(value)

        #description
        description=dom.createElement('description')
        item.appendChild(description)
        value=dom.createCDATASection(blog['description'].encode('utf-8'))
        description.appendChild(value)

        #author
        author=dom.createElement('author')
        item.appendChild(author)
        value=dom.createCDATASection('hankjin')
        author.appendChild(value)

        #pubdate
        pubdate=dom.createElement('pubDate')
        item.appendChild(pubdate)
        value=dom.createTextNode(blog['pubDate'].encode('utf-8'))
        pubdate.appendChild(value)

        #guid
        guid=dom.createElement('guid')
        guid.setAttribute('isPermaLink',"true")
        item.appendChild(guid)
        value=dom.createTextNode(blog['url'])
        guid.appendChild(value)
    dom.writexml(open('163.xml','w'), addindent='  ', newl='\n',encoding='utf-8')

def main():
    blogs = getBlogs()
    generateRSS(blogs)
    
if __name__=='__main__':
    main()

#! usr/bin/env python3
from iPlugin import Plugin
from urllib import request
import chardet
import pymongo
from xml.etree import ElementTree
from lxml import etree

__all__ = ["newsPlugin"]

class newsPlugin(Plugin):
    name = "newsPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)
        uri = 'mongodb://bjl:123456@127.0.0.1/Taxation?authMechanism=SCRAM-SHA-1'
        self.client = pymongo.MongoClient(uri)

        self.db = self.client['Taxation']

        self.collection = self.db["newsContent"]

    def downloade(self,url):
        response = request.urlopen(url)
        html = response.read()
        html = html.decode(chardet.detect(html)['encoding'])
        return html

    def getUrls(self,url,listXpath,titleXpath,postDataXpath,source,contextXpath):
        content = self.downloade(url)
        page = etree.HTML(content)
        hrefs = page.xpath(listXpath)
        for href in hrefs:
            self.dealContent(href,titleXpath,postDataXpath,source,contextXpath)

    def dealContent(self,contentUrl,titleXpath,postDataXpath,source,contextXpath):
        context = self.downloade(contentUrl)

        print(context)

        page = etree.HTML(context)
        title = page.xpath(titleXpath)
        postData = page.xpath(postDataXpath)
        source = source
        contextClean = page.xpath(contextXpath)

        print(title)
        print(postData)
        print(source)
        print(contextClean)

    def getResult(self):
        root = ElementTree.parse("/home/hadoop/pworkspace/pluginSpider/newsConf.xml")
        nodes = root.getiterator("node")

        for node in nodes:
            url = node.find('url').text
            listUrl = node.find('listUrl').text
            title = node.find('title').text
            postDate = node.find('postDate').text
            soucrce = node.find('soucrce').text
            contextXpath = node.find('content').text
            self.getUrls(url,listUrl,title,postDate,soucrce,contextXpath)


if __name__ == '__main__':
    obj = newsPlugin()
    obj.getResult()
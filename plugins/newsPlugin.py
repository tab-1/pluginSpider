#! usr/bin/env python3
from iPlugin import Plugin
from urllib import request
import chardet
import pymongo
from xml.etree import ElementTree
from lxml import etree
import threading

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

    def dealOneSite(self,url,listXpath,titleXpath,postDataXpath,source,contextXpath):
        listContext = self.downloade(url)
        listPage = etree.HTML(listContext)
        hrefs = listPage.xpath(listXpath)
        postDatas = listPage.xpath(postDataXpath)

        for (href,postData) in zip(hrefs,postDatas):
            self.dealContent(href, titleXpath, postData, source, contextXpath)


    def dealContent(self,contentUrl,titleXpath,postData,source,contextXpath):

        print("download:   ",contentUrl)

        context = self.downloade(contentUrl)
        page = etree.HTML(context)
        title = page.xpath(titleXpath)
        source = source
        contextClean = page.xpath(contextXpath)

        print(title)
        print(postData)
        print(source)
        print(contextClean)

    def getResult(self):
        root = ElementTree.parse("/home/hadoop/pworkspace/pluginSpider/newsConf.xml")
        nodes = root.getiterator("node")
        threads = []
        for node in nodes:
            try:
                url = node.find('url').text
                listXpath = node.find('listUrl').text
                titleXpath = node.find('title').text
                postDataXpath = node.find('postDate').text
                source = node.find('source').text
                contextXpath = node.find('content').text

                t = threading.Thread(target=self.dealOneSite,args=(url,listXpath,titleXpath,postDataXpath,source,contextXpath))
                threads.append(t)
            except BaseException:
                print(url + "  Error !!!")

        for t in threads:
            t.setDaemon(True)
            t.start()

        t.join()

if __name__ == '__main__':
    obj = newsPlugin()
    obj.getResult()
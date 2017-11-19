#coding:utf-8
from iPlugin import Plugin
import chardet
import request

class wechatPlugin(Plugin):
    name = "wechatPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def getUrls(self,seedUrl):
        response = request.urlopen(seedUrl)
        html = response.read()
        html = html.decode(chardet.detect(html)['encoding'])

        page = etree.HTML(html)
        hrefs = page.xpath('')
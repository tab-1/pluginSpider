#! usr/bin/env python3

from iPlugin import Plugin
import re #正则表达式
from urllib import request
import urllib.parse
import chardet
import uuid
from lxml import etree

__all__ = ["wechatPlugin"]

class wechatPlugin(Plugin):
    name = "wechatPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def getResult(self, jsonData):
        key = jsonData['key']

        for page in range(1, 10):

            url = 'http://weixin.sogou.com/weixin?hp=0&query=' + urllib.parse.quote(key)\
                  +'&sut=7793&lkt=3%2C1510388289198%2C1510388289961&_sug_=y&sst0=1510388290089&oq=%E5%8F%8C%E7%BF%BC%E6%B5%81&stj0=1&stj1=0&hp1=&stj2=0&stj=1%3B0%3B0%3B0&_sug_type_=&s_from=input&ri=1&type=2'\
                  +'&page=' + str(page) + '&ie=utf8&w=01015002&dr=1'

            response = request.urlopen(url)
            html = response.read()
            html = html.decode(chardet.detect(html)['encoding'])

            page = etree.HTML(html)
            hrefs = page.xpath('//ul[@class="news-list"]//li/div[@class="txt-box"]/h3/a/@href')
            for href in hrefs:
                self.dealContent(href)

    def dealContent(self,href):
        print('begin download ', href)
        doc= {}
        doc['_id'] = uuid.uuid4();

        respone = request.urlopen(href)
        contentHtml = respone.read()
        contentHtml = contentHtml.decode(chardet.detect(contentHtml)['encoding'])

        treeContent = etree.HTML(contentHtml)

        title = treeContent.xpath('//h2[@class="rich_media_title"]//text()')
        postData = treeContent.xpath('//em[@id="post-date"]//text()')
        source = treeContent.xpath('//a[@id="post-user"]//text()')
        contents = treeContent.xpath('//div[@id="js-content"]//text()')

        body = ''
        for content in contents:
            if content.strip() == '':
                continue
            body = body + str(content)

        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filterdata = re.findall(pattern, body)
        cleaned_body = ''.join(filterdata)

        print("title:  ",title[0])
        print("postData:  ", postData)
        print("source:  ", source)
        print("contents:  ", contents)
        print("body:  ", body)
        print("pattern:  ", pattern)
        print("filterdata:  ", filterdata)
        print("cleaned_body:  ", cleaned_body)


if __name__ == '__main__':
    obj = wechatPlugin()
    obj.getResult({"key":"双一流"})

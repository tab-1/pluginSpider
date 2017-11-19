#! usr/bin/env python3
from iPlugin import Plugin
import pymongo
from urllib import request
import urllib.parse
import chardet

__all__ = ["sinaOpinion"]

class sinaOpinion(Plugin):
    name = "sinaOpinion"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)
        uri = 'mongodb://bjl:123456@127.0.0.1/Taxation?authMechanism=SCRAM-SHA-1'
        self.client = pymongo.MongoClient(uri)

        self.db = self.client['Taxation']

        self.collection = self.db["newsContent"]

    def getResult(self,searKey):
        response = request.urlopen('http://s.weibo.com/weibo/' + urllib.parse.quote(searKey) + '&Refer=STopic_box')
        html = response.read()
        # html = html.decode(chardet.detect(html)['encoding'])

        print(html.decode('unicode_escape'))


if __name__ == '__main__':
    obj = sinaOpinion()
    obj.getResult('双一流')
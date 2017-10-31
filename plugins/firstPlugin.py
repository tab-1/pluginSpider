#coding:utf-8
import sys
sys.path.append('../')
import urllib3
import json

from iPlugin import Plugin

__all__ = ["FirstPlugin"]

class FirstPlugin(Plugin):
   
    name = "firstPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):

        print ('begin spider plugin...')

        http_pool = urllib3.PoolManager()
        r = http_pool.request('GET', 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page=2&r=0.8314050882379029')
        print (r.status)
        print (r.data)

    def execFun(self):
        return "exec function"

if __name__ == '__main__':
    jsonData = {"a":1,"b":2,"c":3,"d":4,"e":5}
    print(type(jsonData))
    text = json.loads(jsonData)
    print(type(text))
    print(text)
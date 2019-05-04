#爬取豆瓣悬疑电影排行榜
#利用requests和urllib
#使用代理ip爬取
#将数据用CSV存储
# -*- utf-8 -*-

import requests
import urllib.error
from iptools import head,dict2proxy     
import json
import csv

class DBPQ:
    def __init__(self):
        self.get_date = []      #存储获取的页面数据
        #self.date = []          #存储分类完成的数据

    def get_ip(self):
        """从指定路径获取代理ip"""
        with open('E:\\Python\\爬虫\\ip\\iphq\\proxies.json','r') as f:
            dic = json.load(f)
        return dic

    def get_movie_date(self,index):
        """获取电影数据"""
        urls = []               #不同的页面
        date = []
        dic = self.get_ip()
        ip = dict2proxy(dic[1])

        for i in range(0,index + 20,20):
            urls.append( 'https://movie.douban.com/j/chart/top_list?'           
                         'type=10&interval_id=100%3A90&action=&start={}&limit=20'.format(i))    #数据存储在XHR下的json格式文件

        try:
            for url in urls:        #获取所有页面内容
                res = requests.get(url,headers = head,proxies = ip,timeout = 5)
                res.encoding = 'utf-8'
                self.get_date.append(json.loads(res.text))
        except urllib.error.URLError as e:
            if hasattr(e,'code'):
                print("网络连接错误，原因：{}".format(e.code))
            elif hasattr(e,'reason'):
                print("网络连接错误，原因：{}".format(e.reason))
            else:
                print("连接错误")

        for soups in self.get_date:      #剖析各个数据
            for soup in soups:
                rating = soup['rating'][0]
                jpg_url = soup['cover_url']
                regions = soup['regions']
                title = soup['title']
                movie_url = soup['url']
                date.append({'电影名':title,'评分':rating,'图片':jpg_url,'来源':regions,'电影链接':movie_url})
        return date

    def write_date(self,date):
        """将数据以CSV存储"""
        with open('movie2.csv',mode='w') as f:
            fieldname = ['电影名','评分','图片','来源','电影链接']      #表格头
            writer = csv.DictWriter(f,fieldnames = fieldname)
            writer.writeheader()
            for i in range(len(date)):
                writer.writerow(date[i])

def main():
    """执行函数"""
    m = DBPQ()
    date = m.get_movie_date(60)
    m.write_date(date)

if __name__ == '__main__':
    main()
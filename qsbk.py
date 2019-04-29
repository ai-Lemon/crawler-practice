#爬取糗事百科的内涵段子
#用正则表达式爬取网页
# -*- coding:utf-8 -*-

import re
import urllib.request
import urllib.error

class qsbk:
    def __init__(self):
        self.zt = True        #状态标志
        self.ym = 1           #存放故事的页码
        self.page = 1         #网页的页码
        self.wz = []        #存储整页数据
        self.stories = []   #储存故事
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

    def hqnr(self,page):
        """获取网页内容"""
        try:
            url = ('https://www.qiushibaike.com/text/page/{}/'.format(page))
            headers = {'User-Agent': user_agent}
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            soup = response.read().decode('utf-8')
            return soup
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print('网络连接错误，原因：'.format(e.code))
            if hasattr(e,"reason"):
                print('网络连接失败，原因：'.format(e.reason))

    def jssj(self,page):
        """解析内容，提取出作者与文章"""
        soup = self.hqnr(page)
        pattern = re.compile(r'<div.*?author clearfix".*?<a .*?<img.*?alt=(.*?)>.*?/a>.*?/div>.*?<div.*?content".*?<span>(.*?)</span>.*?/div>',re.S)
        items = re.findall(pattern,soup)
        for item in items:
            replacBR = re.compile('<br/>')
            text = re.sub(replacBR, "\n", item[1])
            self.stories.append([item[0].strip(), text.strip()])
        return self.stories

    def start(self):
        """开始函数"""
        while self.zt:
            self.stories = []
            self.jssj(self.page)
            ym = self.page
            wz = self.stories
            dm = 1
            for i in wz:
                s = input('')
                if s.lower() == 'q':
                    return
                print('第{}页'.format(ym),'第{}段'.format(dm), '作者：{}'.format(i[0]), '\n', i[1])
                dm += 1
            i = input('是否加载下一页？（Y/N）：')
            if i.lower() == 'n':        #若用户按下n则退出
                self.zt = False
                return
            self.page += 1



def main():
    s = qsbk()
    print("按下Enter读取段子，q退出！")
    s.start()


if __name__ == '__main__':
    main()




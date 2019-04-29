#爬取下载王者荣耀英雄皮肤图片
# -*- coding:utf-8 -*-
import requests
import urllib.error

class wz:
    def __init__(self):
        self.here_name = ''
        self.here_number = ''
        self.head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Referer': 'https://pvp.qq.com/web201605/herolist.shtml'}

    def get_name(self,url):
        """提取英雄名字及对数字"""
        try:
            res = requests.get(url, headers=self.head)
            res.encoding = 'utf-8'
            hero_list = res.json()
            self.here_name = list(map(lambda x: x['cname'], hero_list))
            self.here_number = list(map(lambda x: x['ename'], hero_list))
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print('网络连接错误，原因：'.format(e.code))
            if hasattr(e,"reason"):
                print('网络连接失败，原因：'.format(e.reason))

    def save_IMG(self,url):
        """下载并存储图片"""
        num = 0
        h_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'  # 英雄图片的路径
        self.get_name(url)
        # 逐一遍历英雄
        for i in self.here_number:
            # 逐一遍历皮肤，此处假定一个英雄最多有15个皮肤
            for pf_num in range(15):
                # 英雄皮肤的URL链接
                try:
                    pf_url = h_url + str(i) + '/' + str(i) + '-bigskin-' + str(pf_num) + '.jpg'
                    pf_res = requests.get(pf_url)
                except urllib.error.URLError as e:
                    return e
                if pf_res.status_code == 200:
                    # 将图片保存下来，并以"英雄名称_皮肤序号"方式命名
                    with open(self.here_name[num] + str(pf_num) + '.jpg', 'wb') as f:
                        f.write(pf_res.content)
            num = num + 1

def main():
    url = 'https://pvp.qq.com/web201605/js/herolist.json'      #存放英雄名和编号的页面
    s = wz()
    s.save_IMG(url)

if __name__=='__main__':
    main()


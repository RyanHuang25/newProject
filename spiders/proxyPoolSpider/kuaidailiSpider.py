# -*- coding:utf-8 -*-
# @time : 2022/3/18 22:05
# @Author : huangrenwu
# @File : kuaidailiSpider.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

import requests,sys,os
sys.path.append('../')
from lxml import etree
from PipeLine import PipeLine
from tools.Thread_Pool import thread_pool

class KuaidailiSpider:
    '''
    快代理免费代理ip采集
    '''
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }
        self.start_Request()

    def start_Request(self):
        for page in range(1,101):
            url = f'https://www.kuaidaili.com/free/inha/{page}/'
            res = requests.get(url,headers=self.headers)
            tree = etree.HTML(res.text)
            tr_trees = tree.xpath("//div[@id='list']/table//tr")
            for tr_tree in tr_trees:
                thread_pool(self.insert_pipeLine,tr_tree)

    def insert_pipeLine(self,tr_tree):
        try:
            item = {
                "ip": tr_tree.xpath("./td[1]/text()")[0],
                "port": tr_tree.xpath("./td[2]/text()")[0],
            }
            PipeLine().ProxyPipeLine(item)
        except Exception as e:
            print('正在避开标题栏... or {}'.format(e))

if __name__ == "__main__":
    KuaidailiSpider()
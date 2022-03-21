# -*- coding: utf8 -*-
# @Time : 2022/3/21 下午5:13
# @File : sixipSpider.py
# @Author : huangrenwu
# @Email : huangrenwu@handidit.com

import requests,sys
sys.path.append('../../')
from lxml import etree
from PipeLine import PipeLine
from tools.Thread_Pool import thread_pool

class SixipSpider:
    '''66ip免费代理ip采集'''
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }
        self.start_Request()

    def start_Request(self):
        for page in range(1,101):
            url = f'http://www.66ip.cn/{page}.html'
            res = requests.get(url,headers=self.headers)
            tree = etree.HTML(res.text)
            tr_trees = tree.xpath("//div[@class='layui-row layui-col-space15']/div/table//tr")
            for tr_tree in tr_trees:
                if tr_tree.xpath("./td[1]/text()")[0] == "ip":
                    continue
                thread_pool(self.insert_pipeLine, tr_tree)

    def insert_pipeLine(self,tr_tree):
        item = {
            "ip": tr_tree.xpath("./td[1]/text()")[0],
            "port": tr_tree.xpath("./td[2]/text()")[0]
        }
        PipeLine().ProxyPipeLine(item)

if __name__ == "__main__":
    SixipSpider()
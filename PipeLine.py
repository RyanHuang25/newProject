# -*- coding:utf-8 -*-
# @time : 2022/3/13 13:57
# @Author : huangrenwu
# @File : PipeLine.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

from tools.TestProxy import TestProxy
from connect.connect_Redis import connect_Redis
from tools.Redis_Fingerprint import get_md5
from tools.print_color import print_yellow

class PipeLine:
    '''
    数据存储管道
    '''

    def __init__(self):
        '''
        管道初始化设置
        '''
        self.pool = connect_Redis(9)
        self.proxy_pool = "Proxy_Pool"

    def ContactPipeLine(self,item):
        pass

    def ProxyPipeLine(self,item):
        proxies = {
            "http": f"http://{item['ip']}:{item['port']}",
            "https": f"https://{item['ip']}:{item['port']}"
        }
        Exect_Status = self.pool.redis_hexists(self.proxy_pool, get_md5().get_str_md5(proxies['http']))
        if Exect_Status:
            print_yellow('ip exect : {}'.format(proxies))
        else:
            Proxy_Status = TestProxy(proxies)
            if Proxy_Status:
                self.pool.redis_hsex(self.proxy_pool, get_md5().get_str_md5(proxies['http']), proxies)
# -*- coding:utf-8 -*-
# @time : 2022/3/18 17:44
# @Author : huangrenwu
# @File : TestProxy.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com
import json

import requests,sys,platform,random

sys.path.append('../')
from tools.print_color import print_yellow,print_red
from connect.connect_Redis import connect_Redis

redis_pool = connect_Redis(9)
pool_list_name = 'Proxy_Pool'

def TestProxy(proxy):
    '''
    检测代理ip是否有效
    :param proxy: 代理ip
    :return: 代理ip状态
    '''
    # if platform.system() == "Linux":
    ip_url = 'http://47.108.199.19:5050/ip'
    # else:
    #     ip_url = 'http://127.0.0.1:5050/ip'
    try:
        res = requests.get(ip_url,proxies=proxy,timeout=30)
        if res.status_code == 200:
            print(res.text)
            Proxy_Status = True
        else:
            Proxy_Status = False
            print_yellow(f'代理：{proxy["http"]}, 请求状态码：{str(res.status_code)}')
    except Exception as e:
        print_red(f"代理：{proxy['http']},  ERR:{e}")
        Proxy_Status = False
    return Proxy_Status

def Update_Test_Proxy():
    '''
    代理池中代理检测，对无效代理进行删除
    :return:
    '''
    keys = redis_pool.redis_hkeys(pool_list_name)
    for key in keys:
        try:
            proxy = redis_pool.redis_hget(pool_list_name,key)
            proxy = eval(proxy)
            status = TestProxy(proxy)
            print(f'test ip: {proxy}; status: {status}')
            if status:
                pass
            else:
                redis_pool.redis_hdel(pool_list_name,key)
        except Exception as e:
            print_red(e)

def get_proxies():
    keys = redis_pool.redis_hkeys(pool_list_name)
    key = random.choice(keys)
    proxies = redis_pool.redis_hget(pool_list_name,key)
    proxies = eval(proxies)
    return proxies

# Update_Test_Proxy()

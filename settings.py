# -*- coding:utf-8 -*-
# @time : 2022/3/13 13:57
# @Author : huangrenwu
# @File : settings.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com


import platform

if platform.system() == "Linux":
    '''服务器连接断定'''
    CONNECT_TYPE = 'server'
    '''REDIS连接配置'''
    REDIS_HOST = '47.108.199.19'
    REDIS_PORT = 8379
    REDIS_PASSWD = 'spider666.'
else:
    CONNECT_TYPE = 'localhost'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWD = ''

'''mysql连接配置'''
MYSQL_HOST = 'rm-bp10ml3j7a2t88hv03o.mysql.rds.aliyuncs.com'
MYSQL_PORT = 3306
MYSQL_USER = 'roothuang'
MYSQL_PASSWD = 'huang123@'

'''默认爬虫线程池线程数'''
THREAD_POOL_COUNT = 10


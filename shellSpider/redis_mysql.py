# -*- coding: utf8 -*-
# @Time : 2022/3/29 下午6:24
# @File : redis_mysql.py
# @Author : huangrenwu
# @Email : huangrenwu@handidit.com
'''
yellowwebsite 
'''

import sys,threading
sys.path.append('../')

from connect.connect_Redis import connect_Redis
from connect.connect_MySql import ConnectMySql
from tools.Redis_Fingerprint import get_md5

redis_con = connect_Redis(2)
mysql_con = ConnectMySql('huang')


def run():
    while True:
        data = redis_con.redis_lpop('yellowWebsite')
        source_url = data['source_url']
        if 'http' not in source_url:
            source_url = f'http://{source_url}'
        item = {
            "source_url": source_url,
        }
        item['md5'] = get_md5().get_str_md5(source_url)

        mysql_con.insert_data(item,table_name='yellowwebsite')


for i in range(10):
    threading.Thread(target=run).start()


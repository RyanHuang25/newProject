# -*- coding:utf-8 -*-
# @time : 2022/3/14 21:46
# @Author : huangrenwu
# @File : Redis_Fingerprint.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

import hashlib,sys
sys.path.append('../')
from tools.print_color import print_bule
from connect.connect_Redis import connect_Redis

class get_md5:

    def __init__(self):
        pass

    def get_hash_md5(self,item):
        '''
        传入字典，依次取所有值生成md5
        :param item: 需要生成md5的字典
        :return: md5值
        '''
        url = ''
        for value in item.items():
            url += str(value)
        hl = hashlib.md5()
        hl.update(url.encode(encoding='utf8'))
        return hl.hexdigest()

    def get_str_md5(self,url):
        '''
        传入字符串生成md5
        :param url: 需要生成md5的字符串
        :return: md5值
        '''
        hl = hashlib.md5()
        hl.update(url.encode(encoding='utf8'))
        return hl.hexdigest()

class Redis_Fingerprint:

    def __init__(self,db):
        self.pool = connect_Redis(db)
        self.md5 = get_md5()

    def fingerprint_status(self,url,list_name):
        if "dict" in str(type(url)):
            str_md5 = self.md5.get_hash_md5(url)
        else:
            str_md5 = self.md5.get_str_md5(url)
        status = self.pool.redis_hexists(list_name,str_md5)
        if status:
            print_bule(f'指纹已存在：{url}')
        return status

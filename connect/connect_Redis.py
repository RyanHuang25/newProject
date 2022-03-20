# -*- coding:utf-8 -*-
# @time : 2022/3/14 21:56
# @Author : huangrenwu
# @File : connect_Redis.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

import redis,json,sys
sys.path.append('../')
import settings
from tools.print_color import print_green,print_yellow


class connect_Redis:

    host = settings.REDIS_HOST
    port = settings.REDIS_PORT
    passwd = settings.REDIS_PASSWD

    def __init__(self,db):
        self.Pool = redis.ConnectionPool(host=self.host, port=self.port,password=self.passwd,db=db,max_connections=10)

    def conn_redis(self):
        conn = redis.Redis(connection_pool=self.Pool,decode_responses=True)
        return conn

    def redis_lpush(self,list_name,item):
        '''
        向redis中写入list数据，
        :param list_name: list队列名称
        :param item: 字典数据
        :return:
        '''
        conn = self.conn_redis()
        conn.lpush(list_name,json.dumps(item))
        print_green(f'存储数据成功：{item}')

    def redis_lrange(self,list_name,start,end):
        '''
        读取redis中list队列
        :param list_name: list队列名称
        :param start: 读取的其实位置
        :param end:  读取的结束为知
        :return: 列表，未格式化
        '''
        conn = self.conn_redis()
        data_list = conn.lrange(list_name,start,end)
        return data_list

    def redis_lpop(self,list_name):
        '''
        在redis中取出list队列数据
        :param list_name: 队列名称
        :return: 字典
        '''
        conn = self.conn_redis()
        data_json = conn.lpop(list_name)
        data = json.loads(data_json)
        return data

    def redis_hsex(self,hash_name,key,value):
        '''
        向redis中hash队列中key赋值value
        :param hash_name: hash队列
        :param key: 键
        :param value: 值
        :return:
        '''
        conn = self.conn_redis()
        conn.hset(hash_name,key,str(value))
        print_green(f'存储数据成功：{value}')

    def redis_hdel(self,hash_name,key):
        '''
        删除redis中hash队列指定键的值
        :param hash_name: 删除hash队列名称
        :param key: 需要删除的键
        :return:
        '''
        conn = self.conn_redis()
        conn.hdel(hash_name,key)
        print_yellow(f'删除数据成功：{key}')

    def redis_hexists(self,hash_name,key):
        '''
        判断redis中hash是否存在某值
        :param hash_name: hash队列名称
        :param key: 需要删除数据对应的键
        :return:
        '''
        conn = self.conn_redis()
        status = conn.hexists(hash_name,key)
        return status

    def redis_hget(self,hash_name,key):
        '''
        在redis中hash队列中取对应key的值
        :param hash_name: hash队列名称
        :param key: 需要取值的键
        :return:
        '''
        conn = self.conn_redis()
        value = conn.hget(hash_name,key)
        return value.decode()

    def redis_hkeys(self,hash_name):
        '''
        获取redis中hash队列所有的key
        :param hash_name: hash队列名称
        :return: 列表,已格式化
        '''
        conn = self.conn_redis()
        data_keys = conn.hkeys(hash_name)
        keys = [key.decode() for key in data_keys]
        return keys


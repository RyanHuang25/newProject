# -*- coding:utf-8 -*-
# @time : 2022/3/19 14:41
# @Author : huangrenwu
# @File : Thread_Pool.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append('../')
from settings import THREAD_POOL_COUNT
executor = ThreadPoolExecutor(max_workers=THREAD_POOL_COUNT)

def thread_pool(func,arg):
    '''
    线程池
    :param func: 加入线程池方法
    :param arg: 执行方法参数
    :return:
    '''
    task1 = executor.submit(func,arg)
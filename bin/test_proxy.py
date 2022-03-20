# -*- coding:utf-8 -*-
# @time : 2022/3/19 14:48
# @Author : huangrenwu
# @File : test_proxy.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com
import sys,os,platform,threading
sys.path.append('../')
from tools.TestProxy import Update_Test_Proxy
from tools.print_color import print_red


if platform.system() == "Linux":
    python_path = '/usr/bin/python3'
else:
    python_path = '/Library/Frameworks/Python.framework/Versions/3.7/bin/python3'

def proxy_pool_test():
    while True:
        try:
            Update_Test_Proxy()
        except Exception as e:
            print_red(e)

def run_cmd(cmd):
    os.system(cmd)

def proxy_pool_spiders():
    while True:
        try:
            spiders_path = os.getcwd().replace('bin','spiders/proxyPoolSpider')
            spiders_files = os.listdir(spiders_path)
            spiders_thread_list = []
            for spiders_file in spiders_files:
                spiders_cmd = f'{python_path} {spiders_path}/{spiders_file}'
                t = threading.Thread(target=run_cmd,args=(spiders_cmd,))
                spiders_thread_list.append(t)
            for t in spiders_thread_list:
                t.start()
            for t in spiders_thread_list:
                t.join()
        except Exception:
            pass

if __name__ == "__main__":
    threading.Thread(target=proxy_pool_spiders).start()
    threading.Thread(target=proxy_pool_test).start()
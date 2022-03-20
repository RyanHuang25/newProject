# -*- coding:utf-8 -*-
# @time : 2022/3/18 08:54
# @Author : huangrenwu
# @File : print_color.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

def print_red(text):
    print(f'\033[0:31m{text}\033[0m')

def print_bule(text):
    print(f'\033[0;36m{text}\033[0m')

def print_yellow(text):
    print(f'\033[0;33m{text}\033[0m')

def print_green(text):
    print(f'\033[0;32m{text}\033[0m')

# -*- coding: utf8 -*-
'''
@Author : huangrenwu
@File: selenium_work.py
@Time: 2022/6/16 18:02
@Email: leo.r.huang@microcore.tech
@Desc: 
'''
import time

from selenium import webdriver

# 实例化浏览器对象
bro = webdriver.Chrome(executable_path=r'D:/Project/newProject/chromedriver.exe')
url = 'https://yk.myunedu.com'

# 发起请求
bro.get(url)
time.sleep(10)

# 输入登录账户
account_input = bro.find_element_by_id('ddd')
account_input.send_keys('350623199003231014')

passwd_input = bro.find_element_by_id('bbb')
passwd_input.send_keys('KF123456')

bro.find_element_by_class_name('ant-btn btn_login').click()


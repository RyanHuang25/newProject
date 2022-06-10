import json

import requests


class Get_pinyi:
    def __init__(self):
        self.pinyi_url='http://tiqu.pyhttp.taolop.com/getpoolip?count=40&neek=33484&pack=31553&type=2&yys=0&port=1&sb=&mr=0&sep=0&ts=1'
        self.headers={}
        self.test_url='http://www.baidu.com'
        # self.test_url='http://47.108.199.19:5050/ip'

    def get_Pinyi_requests(self):
        res = requests.get(self.pinyi_url)
        data_list = res.json()['data']
        # print(data_list)
        success=0
        for data in data_list:
            # print(data)
            ip = {
                "http": f"http://{data['ip']}:{data['port']}",
            }
            print(ip)
            try:
                rr=requests.get(self.test_url,proxies=ip,timeout=20)
                success+=1
                print(rr)
            except Exception as e:
                print(e)
                pass
        print("共成功",success,"次")
a=Get_pinyi()
a.get_Pinyi_requests()
# -*- coding:utf-8 -*-
# @time : 2022/3/18 17:46
# @Author : huangrenwu
# @File : App_Route.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

from flask import Flask,render_template,request,redirect,url_for
import sys,threading
sys.path.append('../')
from tools.TestProxy import get_proxies
app = Flask(__name__)


@app.route('/proxy')
def get_proxy():
    proxies = get_proxies()
    return proxies

@app.route('/ip')
def getIp():
    ip = request.remote_addr
    ip_item = {
        "status": 200,
        "ip": ip
    }
    return ip_item

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5050,debug=True)
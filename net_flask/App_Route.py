# -*- coding:utf-8 -*-
# @time : 2022/3/18 17:46
# @Author : huangrenwu
# @File : App_Route.py
# @Software : PyCharm
# @Email : huangrenwu@steponeai.com

from flask import Flask,render_template,request,redirect,url_for
import sys,threading
from flask_wtf import Form
from wtforms import StringField, SubmitField
sys.path.append('../')
from tools.TestProxy import get_proxies
from connect.connect_MySql import ConnectMySql

app = Flask(__name__)
con = ConnectMySql('huang')

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

class MockCreate(Form):
    del_btn = SubmitField('del')

@app.route('/y_web',methods=['GET','POST'])
def y_web():
    conn,cursor = ConnectMySql('huang').connect_conn()
    sql = '''SELECT * 
    FROM `yellowwebsite` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM `yellowwebsite`)-(SELECT MIN(id) FROM `yellowwebsite`))+(SELECT MIN(id) FROM `yellowwebsite`)) AS id) AS t2 
    WHERE t1.id >= t2.id 
    ORDER BY t1.id LIMIT 1; 
    '''
    cursor.execute(sql)
    data_list = cursor.fetchall()[0]
    print(data_list[1])
    form = MockCreate()
    # if form.validate_on_submit():
    if request.method == 'post':
        where = {
            "source_url": data_list[1]
        }
        con.del_data('yellowwebsite',where=where)
    return render_template('y_web.html',source_url=data_list[1],form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5050,debug=True)
    # y_web()
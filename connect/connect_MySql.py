# -*- coding: utf8 -*-
# @Time : 2022/3/22 下午4:36
# @File : connect_MySql.py
# @Author : huangrenwu
# @Email : huangrenwu@handidit.com


import pymysql,sys
from DBUtils.PersistentDB import PersistentDB
sys.path.append('../')
import settings
from tools.print_color import print_red,print_green,print_bule,print_yellow

class ConnectMySql:
    '''
    mysql连接池、自动入库
    '''

    def __init__(self,database_name):
        self.pool = PersistentDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            closeable=False,
            # 如果为False时，conn.close() 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close()则关闭链接，那么再次调用pool.connection时就会报错，因为已经真的关闭了连接（pool.steady_connection()可以获取一个新的链接）
            threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWD,
            database=database_name,
            charset="utf8"
        )

    def connect_conn(self):
        '''
        在连接池中获取一个连接
        :return: mysql连接和游标
        '''
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        return conn,cursor

    def get_columns(self,table_name,drop_column):
        '''
        获取mysql中table_name表中所有字段
        :param table_name: 获取字段的表名
        :param drop_column: 自动生成字段
        :return: 字段字典
        '''
        item = {}
        conn,cursor = self.connect_conn()
        sql = "select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name='{}'".format(table_name)
        cursor.execute(sql)
        column_list = cursor.fetchall()
        column_list = [i[0] for i in column_list]
        insert_columns = [i for i in column_list if i not in drop_column]
        for insert_column in insert_columns:
            item[insert_column] = ''
        self.close_conn(conn,cursor)
        return item

    def item_insert_value(self,item_key,item_value):
        '''
        数据和mysql字段进行匹配
        :param item_key:
        :param item_value:
        :return: 返回字典，匹配好的结果
        '''
        for key in item_key.keys():
            try:
                item_key[key] = item_value[key]
            except:
                pass
        return item_key

    def insert_data(self, item, table_name, drop_column=['id', 'updated', 'isonline', 'entid', 'created'],not_empty=[]):
        '''
        写入mysql数据库
        :param item: 数据内容，字典类型
        :param table_name: 表明
        :return:
        '''
        item_key = self.get_columns(table_name, drop_column)
        item = self.item_insert_value(item_key, item)
        values = ''
        for key, value in item.items():
            if key in not_empty:
                if value == "":
                    values += f'"",'
                else:
                    values += f'"{value}",'
            else:
                if value == "":
                    values += f'NULL,'
                else:
                    values += f'"{value}",'
        sql = f'insert into {table_name} ({",".join(item.keys())}) values ({values[:-1]})'
        conn, cursor = self.connect_conn()
        try:
            cursor.execute(sql)
            conn.commit()
            print_green(sql)
        except Exception as e:
            print_red(e)
        self.close_conn(conn, cursor)

    def insert_many(self, item_list, table_name, drop_column=['id', 'updated', 'isonline', 'entid', 'created']):
        '''
        批量入库，操作和自动入库类似
        :param item_list: 数据值列表
        '''
        item_key = self.get_columns(table_name, drop_column)
        conn, cursor = self.connect_conn()
        sss = ''
        for i in range(len(item_key)):
            sss += '%s,'
        sql = 'insert ignore into {} ('.format(table_name) + ','.join(item_key) + ')' + ' values ({})'.format(sss[:-1])

        value_list = []
        for item in item_list:
            for key in item_key.keys():
                try:
                    item_key[key] = item[key]
                except:
                    pass
            data = '(' + ','.join(['%r' % str(i) for i in item_key.values()]) + ')'
            value_list.append(eval(data))
        cursor.executemany(sql, value_list)
        conn.commit()
        self.close_conn(conn, cursor)

    def select_data(self,table_name,where={},limit_count=100):
        '''
        查询数据库
        :param table_name:查询表名
        :param where: 查询条件
        :param limit_count: 最大查询条数
        :return:
        '''
        if where == {}:
            sql = f'select * from {table_name} limit {limit_count}'
        else:
            sql = f'select * from {table_name} where '
            for key,value in where.items():
                sql += f'{key}="{value}" and '
            sql = sql[:-5] + f' limit {limit_count}'
        print_bule(sql)
        conn, cursor = self.connect_conn()
        cursor.execute(sql)
        data_list = cursor.fetchall()
        self.close_conn(conn, cursor)
        return data_list

    def del_data(self,table_name,where):
        if where == {}:
            print_red('请输入删除条件')
            return
        sql = f'delete from {table_name} where '
        for key,value in where.items():
            sql += f'{key}="{value}" and '
        conn, cursor = self.connect_conn()
        cursor.execute(sql[:-5])
        print_yellow(sql[:-5])
        conn.commit()
        self.close_conn(conn, cursor)


    def close_conn(self,conn,cursor):
        cursor.close()
        conn.close()

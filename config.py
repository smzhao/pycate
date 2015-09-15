# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://www.yunsuan.org
'''

import peewee
import socket

def hostname():
    return (socket.gethostname())

menu_arr = [['首页', '/'],
            ['文档', '/category/geography'],
            ['云算', '/calc/find'],
            ['专题', '/spec/'],
]

page_num = 10

site_url = 'http://127.0.0.1:8004'

# 使用DataBase的不同形式，以应对Peewe针对数据库的不同语法
# 1 for SQLite
# 2 for MySQL
# 3 for PostgreSQL
dbtype = 2
# dbconnect = peewee.SqliteDatabase('./database/torcms.db')


dbconnect = peewee.MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = 'g131322', database = 'pycate', )


template_dir_name = 'templates_a'

smtp_cfg = {
    'host': "smtp.ym.163.com",
    'user': "user_name@yunsuan.org",
    'pass': "password_hear",
    'postfix': 'yunsuan.org',
    }



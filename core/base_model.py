# -*- coding:utf-8 -*-

import peewee

from core import config

# create a base model class that our application's models will extend
# 这样我们后面的blog与entry就链接的是同一个数据库了。这个是从django借鉴来的
class BaseModel(peewee.Model):
    class Meta:
        database = peewee.MySQLDatabase(host='127.0.0.1',
                                        user=config.mysql['dbuser'],
                                        password=config.mysql['dbpass'],
                                        database=config.mysql['dbname'])
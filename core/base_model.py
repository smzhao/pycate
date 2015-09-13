# -*- coding:utf-8 -*-

import peewee

# from core import config

import config

# create a base model class that our application's models will extend
# 这样我们后面的blog与entry就链接的是同一个数据库了。这个是从django借鉴来的
class BaseModel(peewee.Model):
    class Meta:
        database = config.dbconnect
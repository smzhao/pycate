# -*- coding:utf-8 -*-
# 预约更新
# import tornpg


import libs
import peewee
from core.base_model import BaseModel


class phpmps_refresh(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='类别的ID', primary_key=True)
    refresh_time = peewee.IntegerField(null=False)
    info_uid = peewee.CharField(max_length=36, null=False)
    time_str = peewee.CharField(max_length=36)


class MRefresh(BaseModel):
    def __init__(self):
        try:
            phpmps_refresh.create_table()
            pass
        except:
            pass

    def getall(self):
        return (phpmps_refresh.select().order_by('cityid'))

    def get_by_id(self, info_id):
        '''
        根据分类的ID进行选择
        '''
        return (phpmps_refresh.select().where(phpmps_refresh.info_uid == info_id))

    def del_by_id(self, uid):
        try:
            entry = phpmps_refresh.delete().where(phpmps_refresh.uid == uid)
            entry.execute()
            return True
        except:
            return False

    def insert_data(self, par_arr):
        uid = libs.tool.get_uid()
        # libs.tool.mark_it()
        try:
            entry = phpmps_refresh.create(
                uid=uid,
                info_uid=par_arr[0],
                refresh_time=par_arr[1],
                time_str=par_arr[2],
            )
            return True
        except:
            return False

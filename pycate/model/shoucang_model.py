# -*- coding:utf-8 -*-
# import tornpg
import libs
import peewee
from core.base_model import BaseModel


class phpmps_shoucang(BaseModel):
    userid = peewee.CharField(max_length=36)
    info_uid = peewee.CharField(max_length=36, null=False)
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='类别的ID', primary_key=True)
    timestamp = peewee.IntegerField()
    title = peewee.CharField(max_length=255, null=True)
    catname = peewee.CharField(max_length=255, null=True)
    timestamp_str = peewee.CharField(max_length=60)


class MShoucang(BaseModel):
    def __init__(self):
        try:
            phpmps_shoucang.create_table()
            pass
        except:
            pass

    def has_record(self, uid):
        try:
            phpmps_shoucang.get(uid=uid)
            return (True)
        except:
            return (False)

    def get_by_userid(self, userid):
        return (phpmps_shoucang.select().where(phpmps_shoucang.userid == userid))  # .order_by('timestamp'))

    def del_by_id(self, uid):
        entry = phpmps_shoucang.delete().where(phpmps_shoucang.uid == uid)
        entry.execute()

    def insert_data(self, par_arr):

        entry = phpmps_shoucang.create(
            uid=par_arr['uid'],
            userid=par_arr['userid'],
            info_uid=par_arr['info_uid'],
            timestamp=par_arr['timestamp'],
            title=par_arr['title'],
            catname=par_arr['catname'],
        )
        return



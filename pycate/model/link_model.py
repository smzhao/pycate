# -*- coding:utf-8 -*-
# import tornpg

import uuid
import peewee
from core.base_model import BaseModel


class phpmps_link(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='类别的ID', primary_key=True)
    webname = peewee.CharField(max_length=60, null=False, help_text='类别中文名称')
    url = peewee.CharField(max_length=50, null=False, )
    linkorder = peewee.IntegerField(null=False)
    logo = peewee.CharField(max_length=50, null=False, )
    img = peewee.CharField(max_length=50)
    catid = peewee.CharField(max_length=4)
    cityid = peewee.CharField(max_length=30)
    parentid = peewee.CharField(max_length=4)
    username = peewee.CharField(max_length=255)


# from model.dblite_model import DatabaseLite


class MLink(BaseModel):
    def __init__(self, cityname):
        # phpmps_category.create_table()
        try:
            # phpmps_link.create_table()
            pass
        except:
            pass
        self.city_name = cityname

    def insert_rec(self, data):
        entry = phpmps_link.create(
            uid=uuid.uuid1(),
            catid=data['catid'],
            img=data['img'],
            webname='',
            url=data['url'],
            linkorder=0,
            logo='',
            cityid=data['cityid'],
            parentid=data['parentid'],
            username=data['username'],
        )


    def update(self, uid, post_data):
        entry = phpmps_link.update(
            catid=post_data['catid'],
            img=post_data['img'],
            url=post_data['url'],
        ).where(phpmps_link.uid == uid)
        entry.execute()

    def get_links(self):
        # sql_cmd = "select * from phpmps_link "

        return (phpmps_link.select())

    def get_links_by_catid(self, catid):
        # sql_cmd = "select * from phpmps_link where catid='%s'" % (catid)
        return (phpmps_link.select().where(phpmps_link.catid == catid))

    def get_links_by_cityid(self, userid, cityid):
        # sql_cmd = "select * from phpmps_link where username='{0}' and cityid='{1}' ".format(userid, cityid)
        return (phpmps_link.select().where((phpmps_link.username == userid) & (phpmps_link.cityid == cityid)))

    def get_links_by_parentid(self, parentid, user_name=''):
        if user_name == '':
            return False
        try:
            print(parentid)
            print(user_name)
            print(self.city_name)
            return phpmps_link.get((phpmps_link.parentid == parentid) & (phpmps_link.username == user_name) & (
                phpmps_link.cityid == self.city_name))
        except:
            return False

    def query_links_by_parentid(self, parentid):
        try:
            return phpmps_link.select().where((phpmps_link.parentid == parentid) & (
                phpmps_link.cityid == self.city_name))
        except:
            return False

    def get_by_id(self, link_id):
        # field_dic = ['uid', 'url', 'img', 'catid', 'cityid']
        # self.db.get("select {0} from phpmps_link  where uid='{1}'".format(','.join(field_dic), link_id))
        return (phpmps_link.get(uid=link_id))


    def delete_by_uid(self, uid):
        # sql_cmd = "delete from phpmps_link where uid='%s'" % (uid)
        entry = phpmps_link.delete().where(phpmps_link.uid == uid)
        entry.execute()




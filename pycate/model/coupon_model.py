# # -*- coding:utf-8 -*-
# # import tornpg
# import peewee
# from core.base_model import BaseModel
# class phpmps_coupon(BaseModel):
#     uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='类别的ID', primary_key=True)
#     title = peewee.CharField(max_length=255, null=False, help_text='类别中文名称')
#     address = peewee.CharField(max_length=255, null=False, )
#     company = peewee.CharField(max_length=255, null=False, )
#     count = peewee.IntegerField(null=False)
#     user_name = peewee.CharField(max_length=255)
#
#
# class MCoupon(BaseModel):
#     def __init__(self):
#         try:
#             phpmps_coupon.create_table()
#             pass
#         except:
#             pass
#
#     def getall(self):
#
#         db_data = phpmps_coupon.select().limit(10)
#         return (db_data)
#
#     def get_by_id(self, uid):
#         return phpmps_coupon.get(uid=uid)
#
#     def has_record(self,uid):
#         tt = self.get_by_id(uid)
#         if len(tt) == 0:
#             return(False)
#         return(True)
#
#     def get_by_userid(self, userid):
#         uu = self.db.query("select * from phpmps_coupon  where userid='{0}' order by timestamp desc ".format(userid))
#         return (uu)
#     def del_by_id(self, uid):
#         sql_cmd = '''DELETE FROM phpmps_coupon WHERE uid='{0}'; '''.format(uid)
#         self.db.execute(sql_cmd)
#     def insert_data(self, par_arr):
#         sql_str = '''insert into phpmps_coupon (uid, userid, info_uid, timestamp, title)
#           values ('{0}', '{1}', '{2}',{3}, '{4}')
#           '''.format(par_arr['uid'], par_arr['userid'], par_arr['info_uid'],
#                      par_arr['timestamp'], par_arr['title'])
#         self.db.execute(sql_str)
#         return

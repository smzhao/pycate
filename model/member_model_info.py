# -*- coding:utf-8 -*-
import uuid
import time
# from core import config

# from model.dblite_model import DatabaseLite
import libs.tool
import libs
import peewee
from core.base_model import BaseModel
from core.config import c


class phpmps_member_info(BaseModel):
    user_name = peewee.CharField(max_length=36, null=False, unique=True, help_text='类别的ID', primary_key=True)
    email = peewee.CharField(max_length=60)
    user_pass = peewee.CharField(max_length=32)
    register_time = peewee.IntegerField()
    registerip = peewee.CharField(max_length=15)
    lastlogintime = peewee.IntegerField()
    lastloginip = peewee.CharField(max_length=15)
    sendmailtime = peewee.IntegerField()
    qq = peewee.CharField(max_length=36)
    phone = peewee.CharField(max_length=36)
    address = peewee.CharField(max_length=100)
    mappoint = peewee.CharField(max_length=50)

    is_vip = peewee.BooleanField(null=True, help_text='是否VIP')
    is_credit = peewee.BooleanField(null=True, help_text='是否经过认证')
    is_personal = peewee.BooleanField(null=True, help_text='是否是个人')
    vip_cat = peewee.CharField(max_length=255, null=False, default='', help_text='VIP具备的类别')
    img_touxiang = peewee.CharField(max_length=255, null=False, default='')
    is_zhizhao = peewee.BooleanField(null=True)
    img_credit = peewee.CharField(max_length=255, null=False, default='')
    img_zhizhao = peewee.CharField(max_length=255, null=False, default = '', help_text='执照')

    chenghu = peewee.CharField(max_length=50, null=True)
    last_keyword = peewee.CharField(max_length=255, null=True)
    coupon_uid = peewee.CharField(max_length=36, null=True)
    coupon_status = peewee.IntegerField(null=True)
    coupon_timestamp = peewee.IntegerField(null=True)
    coupon_num = peewee.IntegerField(null=True)
    login_timestamp = peewee.IntegerField(null=True, help_text='上次登陆时间')
    coupon_last_timestamp = peewee.IntegerField(null=True)
    cname = peewee.CharField(max_length=50, null=True, help_text='中文姓名')
    sex = peewee.IntegerField(null=True)


class MUserInfo(BaseModel):
    def __init__(self, uname):

        try:
            phpmps_member_info.create_table()
        except:
            pass
        self.uname = uname

    def set_vip(self, user_id):
        entry = phpmps_member_info.update(
            is_vip=True
        ).where(user_uid=user_id)
        entry.execute()

    def set_credit(self, user_id):
        entry = phpmps_member_info.update(
            is_credit=True
        ).where(phpmps_member_info.user_uid == user_id)
        entry.execute()

    def set_last_keyword(self, keyword):
        entry = phpmps_member_info.update(
            last_keyword=keyword
        ).where(phpmps_member_info.user_name == self.uname)
        entry.execute()

    def get_last_keyword(self):
        return (phpmps_member_info.get(user_name=self.uname).last_keyword)

    # def num_decrease(self, sig):
    # # print(sig)
    #     if 'refresh' == sig:
    #         self.refresh_num_decrease()
    #     elif 'zhiding' == sig:
    #         self.zhiding_num_decrease()
    #     elif 'tuiguang' == sig:
    #         self.tuiguang_num_decrease()
    #     elif 'yuyue' == sig:
    #         self.yuyue_num_decrease()

    # 下面4个函数处理 refresh
    # def get_free_refresh_num(self):
    #     return phpmps_member_info.get(user_name=self.uname).free_refresh_num
    #
    # def get_vip_refresh_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).vip_refresh_num)
    #
    # def get_buy_refresh_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).buy_refresh_num)

    # def get_refresh_num(self):
    #     return self.get_free_refresh_num() + self.get_vip_refresh_num() + self.get_buy_refresh_num()
    #
    # def get_yuyue_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).vip_yuyue_num)

    # def get_refresh_last_timestamp(self):
    #     return (phpmps_member_info.get(user_name=self.uname).free_refresh_timestamp)


    def is_vip(self):
        if self.uname == '':
            return False
        if phpmps_member_info.get(user_name=self.uname).is_vip == 1:
            return True
        else:
            return False

    def get_vip_cats(self):
        uu = self.get_by_username()
        vip_cat = uu.vip_cat.strip().split(',')
        if vip_cat == ['']:
            vip_cat = []

        return (vip_cat)


    # def refresh_num_decrease(self):
    #     ss = self.get_free_refresh_num()
    #     tt = self.get_vip_refresh_num()
    #     uu = self.get_buy_refresh_num()
    #     print(ss)
    #     print(tt)
    #     print(uu)
    #     if ss + tt + uu == 0:
    #         return False
    #     if ss > 0:
    #         entry = phpmps_member_info.update(free_refresh_num=ss - 1,
    #                                           free_refresh_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #     if tt > 0:
    #         entry = phpmps_member_info.update(vip_refresh_num=tt - 1,
    #                                           vip_refresh_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #
    #     if uu > 0:
    #         entry = phpmps_member_info.update(buy_refresh_num=uu - 1,
    #                                           buy_refresh_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #     return False
    #
    #
    # def reset_refresh_num(self):
    #     user_rec = self.get_by_username()
    #     free_refresh_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.free_refresh_timestamp))
    #     vip_refresh_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.vip_refresh_timestamp))
    #     current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    #
    #     if (free_refresh_date != current_date):
    #         entry = phpmps_member_info.update(
    #             free_refresh_num=c.free_refresh_num_a_day,
    #             free_refresh_timestamp=libs.tool.get_timestamp()
    #         ).where(phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #     if user_rec.is_vip == 1 and (vip_refresh_date != current_date ):
    #         entry = phpmps_member_info.update(
    #             vip_refresh_num=c.vip_refresh_num_a_day,
    #             vip_refresh_timestamp=libs.tool.get_timestamp()
    #         ).where(phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #
    # def reset_publish_num(self):
    #     user_rec = self.get_by_username()
    #     free_publish_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.free_publish_timestamp))
    #     vip_publish_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.vip_publish_timestamp))
    #     current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    #
    #     if (free_publish_date != current_date):
    #         entry = phpmps_member_info.update(
    #             free_publish_num=c.free_publish_num_a_day,
    #             free_publish_timestamp=libs.tool.get_timestamp()
    #         ).where(phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #     if user_rec.is_vip == 1 and (vip_publish_date != current_date ):
    #         entry = phpmps_member_info.update(
    #             vip_publish_num=c.vip_publish_num_a_day,
    #             vip_publish_timestamp=libs.tool.get_timestamp()
    #         ).where(phpmps_member_info.user_name == self.uname)
    #         entry.execute()

    # def reset_tuiguang_num(self):
    #     user_rec = self.get_by_username()
    #     vip_tuiguang_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.vip_tuiguang_timestamp))
    #     current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    #     if user_rec.is_vip == 1 and (vip_tuiguang_date != current_date ):
    #         entry = phpmps_member_info.update(
    #             vip_tuiguang_num=c.vip_tuiguang_num_a_day,
    #             vip_tuiguang_timestamp=libs.tool.get_timestamp()
    #         ).where(phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #
    # def reset_yuyue_num(self):
    #     user_rec = self.get_by_username()
    #     vip_yuyue_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.vip_yuyue_timestamp))
    #     current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
    #     if user_rec.is_vip == 1 and (vip_yuyue_date != current_date ):
    #         entry = phpmps_member_info.update(
    #             vip_yuyue_num=c.vip_yuyue_num_a_day,
    #             vip_yuyue_timestamp=libs.tool.get_timestamp()
    #         ).where(phpmps_member_info.user_name == self.uname)
    #         entry.execute()

    # def get_buy_zhiding_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).buy_zhiding_num)
    #
    #
    # def get_zhiding_num(self):
    #     return self.get_buy_zhiding_num()
    #
    # def zhiding_num_decrease(self):
    #     # tt = self.get_vip_zhiding_num()
    #     uu = self.get_buy_zhiding_num()
    #     if uu == 0:
    #         return False
    #
    #     if uu > 0:
    #         entry = phpmps_member_info.update(buy_zhiding_num=uu - 1,
    #                                           buy_zhiding_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #     return False

    # 下面处理置顶
    # def get_buy_tuiguang_num(self):
    # return (phpmps_member_info.get(user_name=self.uname).buy_tuiguang_num)

    # def get_vip_tuiguang_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).vip_tuiguang_num)

    # def get_tuiguang_num(self):
    #     # return self.get_buy_tuiguang_num() + self.get_vip_tuiguang_num()
    #     return self.get_vip_tuiguang_num()

    # def tuiguang_num_decrease(self):
    #     tt = self.get_vip_tuiguang_num()
    #     # uu = self.get_buy_tuiguang_num()
    #     if tt == 0:
    #         return False
    #     if tt > 0:
    #         entry = phpmps_member_info.update(vip_tuiguang_num=tt - 1,
    #                                           vip_tuiguang_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #
    #     return False

    def yuyue_num_decrease(self):
        tt = self.get_yuyue_num()
        # uu = self.get_buy_tuiguang_num()
        if tt == 0:
            return False
        if tt > 0:
            entry = phpmps_member_info.update(vip_yuyue_num=tt - 1,
                                              vip_yuyue_timestamp=libs.tool.get_timestamp()).where(
                phpmps_member_info.user_name == self.uname)
            entry.execute()
            return True

        return False

    def yuyue_num_increase(self):
        tt = self.get_yuyue_num()
        entry = phpmps_member_info.update(vip_yuyue_num=tt + 1,
                                          vip_yuyue_timestamp=libs.tool.get_timestamp()).where(
            phpmps_member_info.user_name == self.uname)
        entry.execute()
        return True

    # 下面4个函数处理 publish
    # def get_free_publish_num(self):
    #     print(self.uname)
    #     return (phpmps_member_info.get(user_name=self.uname).free_publish_num)
    #
    # def get_vip_publish_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).vip_publish_num)
    #
    # def get_buy_publish_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).buy_publish_num)
    #
    # def get_publish_last_timestamp(self):
    #     return (phpmps_member_info.get(user_name=self.uname).free_publish_timestamp)
    #
    #
    # def get_jinbi_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).def_jinbi)
    #
    # def get_jifen_num(self):
    #     return (phpmps_member_info.get(user_name=self.uname).def_jifen)

    # def publish_num_decrease(self):
    # def publish_num_decrease(self):
    # ss = self.get_free_publish_num()
    #     tt = self.get_vip_publish_num()
    #     uu = self.get_buy_publish_num()
    #     if ss + tt + uu == 0:
    #         return False
    #     if ss > 0:
    #         entry = phpmps_member_info.update(free_publish_num=ss - 1,
    #                                           free_publish_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #     if tt > 0:
    #         entry = phpmps_member_info.update(vip_publish_num=tt - 1,
    #                                           vip_publish_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #
    #     if uu > 0:
    #         entry = phpmps_member_info.update(buy_publish_num=uu - 1,
    #                                           buy_publish_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_info.user_name == self.uname)
    #         entry.execute()
    #         return True
    #     return False

    # def publish_num_reset(self):
    #     entry = phpmps_member_info.update(
    #         free_publish_num=c.publish_num_a_day,
    #         free_publish_timestamp=libs.tool.get_timestamp()
    #     ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()

    def get_coupon_last_timestamp(self):
        return (phpmps_member_info.get(user_name=self.uname).coupon_last_timestamp)

    def get_remain_coupon_num(self):
        return (phpmps_member_info.get(user_name=self.uname).coupon_num)

    def coupon_reset(self):
        entry = phpmps_member_info.update(
            coupon_num=c.coupon_num_a_day,
            coupon_last_timestamp=libs.tool.get_timestamp()
        ).where(phpmps_member_info.user_name == self.uname)
        entry.execute()

    def login_stamp_update(self):
        entry = phpmps_member_info.update(
            login_timestamp=libs.tool.get_timestamp()
        ).where(phpmps_member_info.user_name == self.uname)
        entry.execute()


    def coupon_num_decrease(self):
        tt = self.get_remain_coupon_num()
        if tt > 0:
            entry = phpmps_member_info.update(
                coupon_num=tt - 1,
                coupon_last_timestamp=libs.tool.get_timestamp(),
            ).where(phpmps_member_info.user_name == self.uname)
            entry.execute()

    # def jifen_increase(self, num=1):
    #     # tt = self.get_by_username(u_name).def_jifen
    #     tt = phpmps_member_info.get(user_name=self.uname).def_jifen
    #     entry = phpmps_member_info.update(def_jifen=tt + num, ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()

    def get_by_username(self):
        if self.uname == '':
            return False
        return (phpmps_member_info.get(user_name=self.uname))

    def get_by_tel(self, tel):
        return (phpmps_member_info.get(phone=tel))

    def update_touxiang(self, imagepath):
        try:
            entry = phpmps_member_info.update(
                img_touxiang=imagepath,
            ).where(phpmps_member_info.user_name == self.uname)
            entry.execute()
            return (True)
        except:
            return (False)

    def update_renzheng(self, imagepath):
        try:
            entry = phpmps_member_info.update(
                img_credit=imagepath,
            ).where(phpmps_member_info.user_name == self.uname)
            entry.execute()
            return (True)
        except:
            return (False)

    # def charge(self, amount):
    #     jinbi = amount * c.rmb2jinbi + self.get_jinbi_num()
    #     entry = phpmps_member_info.update(
    #         def_jinbi=jinbi,
    #     ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()
    #     return (True)

    # def convert(self, amount):
    #     jifen = self.get_jifen_num() - amount * c.jinbi2jifen
    #     if jifen < 0:
    #         return False
    #     jinbi = self.get_jinbi_num() + amount
    #     entry = phpmps_member_info.update(
    #         def_jinbi=jinbi,
    #         def_jifen=jifen,
    #     ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()
    #     return (True)

    # def buy_refresh(self, amount):
    #     current_jinbi = self.get_jinbi_num()
    #     if amount > current_jinbi:
    #         return False
    #     refresh_num = amount * c.jinbi2refresh + self.get_buy_refresh_num()
    #     entry = phpmps_member_info.update(
    #         buy_refresh_num=refresh_num,
    #         def_jinbi=self.get_jinbi_num() - amount,
    #     ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()
    #     return (True)
    #
    # def buy_publish(self, amount):
    #     current_jinbi = self.get_jinbi_num()
    #     if amount > current_jinbi:
    #         return False
    #     publish_num = amount * c.jinbi2publish + self.get_buy_publish_num()
    #     entry = phpmps_member_info.update(
    #         buy_publish_num=publish_num,
    #         def_jinbi=self.get_jinbi_num() - amount,
    #     ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()
    #     return (True)

    # def buy_zhiding(self, amount):
    #     current_jinbi = self.get_jinbi_num()
    #     if amount > current_jinbi:
    #         return False
    #     zhiding_num = amount * c.jinbi2zhiding + self.get_buy_zhiding_num()
    #     entry = phpmps_member_info.update(
    #         buy_zhiding_num=zhiding_num,
    #         def_jinbi=self.get_jinbi_num() - amount,
    #     ).where(phpmps_member_info.user_name == self.uname)
    #     entry.execute()
    #     return (True)

    def update_password(self, new_password):
        try:
            entry = phpmps_member_info.update(
                user_pass=libs.tool.md5(new_password),
            ).where(phpmps_member_info.user_name == self.uname)
            entry.execute()
            return (True)
        except:
            return (False)
        return (False)


    def update_userinfo(self, post_data):
        entry = phpmps_member_info.update(
            email=post_data['email'][0],
            phone=post_data['tel'][0],
            cname=post_data['cname'][0],
            sex=post_data['sex'][0],
            qq=post_data['qq'][0]
        ).where(phpmps_member_info.user_name == self.uname)
        entry.execute()

    def update_coupon(self, info_dic):
        entry = phpmps_member_info.update(
            coupon_uid=info_dic['coupon_uid'],
            coupon_timestamp=info_dic['coupon_timestamp'],

        ).where(phpmps_member_info.user_name == info_dic['userid'])
        entry.execute()

    def delete_user(self):
        query = phpmps_member_info.delete().where(phpmps_member_info.user_name == self.uname)
        query.execute()  # Returns the number of rows deleted.


    def insert_data(self, post_data):
        entry = phpmps_member_info.create(
            user_name=post_data['user_name'][0],
            user_pass=libs.tool.md5(post_data['user_pass'][0]),
            # user_uid=uuid.uuid1(),
            register_time=libs.tool.get_timestamp(),
            is_credit=False,
            is_vip=False,
            is_personal=True,

            email=post_data['xemail'][0],
            phone=post_data['xtel'][0],


            refresh_last_timestamp=time.time(),

            def_publish_num=5,
            def_publish_now=time.time(),
            publish_remain_num=5,
            publish_last_timestamp=time.time(),
        )


    def check_user_pass(self, uname, user_pass):
        print(uname)
        print(user_pass)

        res = phpmps_member_info.get(user_name=uname)
        print(res)
        # except:
        #     return False
        # print(res.user_pass)
        # print(user_pass)
        if res.user_pass == user_pass:
            return True
        return False



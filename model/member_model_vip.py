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


class phpmps_member_vip(BaseModel):
    user_name = peewee.CharField(max_length=36, null=False, help_text='类别的ID', )
    parentid = peewee.CharField(max_length=4, null=False, )
    publish_num = peewee.IntegerField()
    publish_timestamp = peewee.IntegerField()
    refresh_num = peewee.IntegerField()
    refresh_timestamp = peewee.IntegerField()
    tuiguang_num = peewee.IntegerField()
    tuiguang_timestamp = peewee.IntegerField()
    yuyue_num = peewee.IntegerField()
    yuyue_timestamp = peewee.IntegerField()


class MUserVip(BaseModel):
    def __init__(self, uname):
        try:
            phpmps_member_vip.create_table()
        except:
            pass
        self.uname = uname


    def set_vip(self, user_id):
        entry = phpmps_member_vip.update(
            is_vip=True
        ).where(user_uid=user_id)
        entry.execute()

    def set_credit(self, user_id):
        entry = phpmps_member_vip.update(
            is_credit=True
        ).where(phpmps_member_vip.user_uid == user_id)
        entry.execute()

    def set_last_keyword(self, keyword):
        entry = phpmps_member_vip.update(
            last_keyword=keyword
        ).where(phpmps_member_vip.user_name == self.uname)
        entry.execute()

    def get_last_keyword(self):
        return (phpmps_member_vip.get(user_name=self.uname).last_keyword)

    def num_decrease(self, sig, parentid=''):
        # print(sig)
        if parentid == '':
            return False
        if 'refresh' == sig:
            self.refresh_num_decrease(parentid)
        elif 'zhiding' == sig:
            self.zhiding_num_decrease(parentid)
        elif 'tuiguang' == sig:
            self.tuiguang_num_decrease(parentid)
        elif 'yuyue' == sig:
            self.yuyue_num_decrease(parentid)

    # 下面4个函数处理 refresh
    # def get_free_refresh_num(self):
    # return phpmps_member_vip.get(user_name=self.uname).free_refresh_num

    # def get_vip_refresh_num(self):


    # def get_buy_refresh_num(self):
    #     return (phpmps_member_vip.get(user_name=self.uname).refresh_num)

    def get_refresh_num(self):
        return (phpmps_member_vip.get(user_name=self.uname).refresh_num)
        # return self.get_free_refresh_num() + self.get_vip_refresh_num() + self.get_buy_refresh_num()

    def get_yuyue_num(self):
        return (phpmps_member_vip.get(user_name=self.uname).yuyue_num)

    def get_refresh_last_timestamp(self):
        return (phpmps_member_vip.get(user_name=self.uname).free_refresh_timestamp)


    # def is_vip(self):
    # if phpmps_member_vip.get(user_name=self.uname).is_vip == 1:
    # return True
    # else:
    # return False


    def refresh_num_decrease(self, parendid=''):
        if parendid == '':
            return False
        tt = self.get_refresh_num()
        if tt > 0:
            entry = phpmps_member_vip.update(refresh_num=tt - 1,
                                             refresh_timestamp=libs.tool.get_timestamp()).where(
                (phpmps_member_vip.user_name == self.uname) & ( phpmps_member_vip.parentid == parendid))
            entry.execute()
            return True

        return False

    def init_vip_num(self, vip_cat):
        ts = libs.tool.get_timestamp()
        phpmps_member_vip.create(
            user_name=self.uname,
            parentid=vip_cat,
            refresh_num=c.vip_refresh_num_a_day,
            refresh_timestamp=ts,
            publish_num=c.vip_publish_num_a_day,
            publish_timestamp=ts,
            tuiguang_num=c.vip_tuiguang_num_a_day,
            tuiguang_timestamp=ts,
            yuyue_num=c.vip_yuyue_num_a_day,
            yuyue_timestamp=ts,
        )


    def reset_refresh_num(self, vip_cats):
        for vip_cat in vip_cats:
            user_rec = self.get_by_parentid(vip_cat)
            if user_rec is None:
                self.init_vip_num(vip_cat)
            else:
                vip_refresh_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.refresh_timestamp))
                current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

                if (vip_refresh_date != current_date ):
                    entry = phpmps_member_vip.update(
                        refresh_num=c.vip_refresh_num_a_day,
                        refresh_timestamp=libs.tool.get_timestamp()
                    ).where((phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == vip_cat))
                    entry.execute()

    def reset_publish_num(self, vip_cats):
        for vip_cat in vip_cats:
            user_rec = self.get_by_parentid(vip_cat)

            if user_rec is None:
                pass
            else:

                vip_publish_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.publish_timestamp))
                current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

                if (vip_publish_date != current_date ):
                    entry = phpmps_member_vip.update(
                        publish_num=c.vip_publish_num_a_day,
                        publish_timestamp=libs.tool.get_timestamp()
                    ).where((phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == vip_cat))
                    entry.execute()

    def reset_tuiguang_num(self, vip_cats):
        for vip_cat in vip_cats:
            user_rec = self.get_by_parentid(vip_cat)
            if user_rec is None:
                pass
            else:

                vip_tuiguang_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.tuiguang_timestamp))
                current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

                if (vip_tuiguang_date != current_date ):
                    entry = phpmps_member_vip.update(
                        tuiguang_num=c.vip_tuiguang_num_a_day,
                        tuiguang_timestamp=libs.tool.get_timestamp()
                    ).where((phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == vip_cat))
                    entry.execute()

    def reset_yuyue_num(self, vip_cats):
        for vip_cat in vip_cats:
            user_rec = self.get_by_parentid(vip_cat)
            if user_rec is None:
                pass
            else:

                vip_yuyue_date = time.strftime("%Y-%m-%d", time.localtime(user_rec.yuyue_timestamp))
                current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

                if (vip_yuyue_date != current_date ):
                    entry = phpmps_member_vip.update(
                        yuyue_num=c.vip_yuyue_num_a_day,
                        yuyue_timestamp=libs.tool.get_timestamp()
                    ).where((phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == vip_cat))
                    entry.execute()

    # def get_buy_zhiding_num(self):
    #     return (phpmps_member_vip.get(user_name=self.uname).buy_zhiding_num)
    #
    #
    # def get_zhiding_num(self):
    #     return self.get_buy_zhiding_num()

    # def zhiding_num_decrease(self):
    # # tt = self.get_vip_zhiding_num()
    # uu = self.get_buy_zhiding_num()
    # if uu == 0:
    # return False
    #
    # if uu > 0:
    #         entry = phpmps_member_vip.update(buy_zhiding_num=uu - 1,
    #                                          buy_zhiding_timestamp=libs.tool.get_timestamp()).where(
    #             phpmps_member_vip.user_name == self.uname)
    #         entry.execute()
    #         return True
    #     return False

    # 下面处理置顶
    # def get_buy_tuiguang_num(self):
    # return (phpmps_member.get(user_name=self.uname).buy_tuiguang_num)



    def get_tuiguang_num(self, parentid):
        # return self.get_buy_tuiguang_num() + self.get_vip_tuiguang_num()
        return (phpmps_member_vip.get(
            (phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == parentid)).tuiguang_num)

    def tuiguang_num_decrease(self, parenid):
        tt = self.get_tuiguang_num(parenid)
        # uu = self.get_buy_tuiguang_num()
        if tt == 0:
            return False
        if tt > 0:
            entry = phpmps_member_vip.update(tuiguang_num=tt - 1,
                                             tuiguang_timestamp=libs.tool.get_timestamp()).where(
                (phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == parenid))
            entry.execute()
            return True

        return False

    def yuyue_num_decrease(self, parentid):
        tt = self.get_yuyue_num()
        # uu = self.get_buy_tuiguang_num()
        if tt == 0:
            return False
        if tt > 0:
            entry = phpmps_member_vip.update(yuyue_num=tt - 1,
                                             yuyue_timestamp=libs.tool.get_timestamp()).where(
                phpmps_member_vip.user_name == self.uname)
            entry.execute()
            return True

        return False

    def yuyue_num_increase(self, parentid):
        tt = self.get_yuyue_num()
        entry = phpmps_member_vip.update(yuyue_num=tt + 1,
                                         yuyue_timestamp=libs.tool.get_timestamp()).where(
            (phpmps_member_vip.user_name == self.uname) &(phpmps_member_vip.parentid == parentid))
        entry.execute()
        return True

    # 下面4个函数处理 publish
    # def get_free_publish_num(self):
    #     return (phpmps_member_vip.get(user_name=self.uname).free_publish_num)

    def get_vip_publish_num(self, parentid):
        user_rec = self.get_by_parentid(parentid)
        # print('=' * 80)
        # print(user_rec)
        # print(parentid)
        # print(user_rec.user_name)
        # print(user_rec.parentid)
        if user_rec is None:
            self.init_vip_num(parentid)

        return (phpmps_member_vip.get(
            (phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == parentid)).publish_num)

    # def get_buy_publish_num(self):
    #     return (phpmps_member_vip.get(user_name=self.uname).buy_publish_num)

    def get_publish_last_timestamp(self):
        return (phpmps_member_vip.get(user_name=self.uname).publish_timestamp)


    # def get_jinbi_num(self):
    #     return (phpmps_member_vip.get(user_name=self.uname).def_jinbi)
    #
    # def get_jifen_num(self):
    #     return (phpmps_member_vip.get(user_name=self.uname).def_jifen)

    # def publish_num_decrease(self):
    def publish_num_decrease(self, parentid):
        tt = self.get_vip_publish_num(parentid)
        if tt == 0:
            return False
        if tt > 0:
            entry = phpmps_member_vip.update(publish_num=tt - 1,
                                             publish_timestamp=libs.tool.get_timestamp()).where(
                (phpmps_member_vip.user_name == self.uname) & (phpmps_member_vip.parentid == parentid))
            entry.execute()
            return True

        return False

    # def publish_num_reset(self):
    #     entry = phpmps_member_vip.update(
    #         publish_num=c.publish_num_a_day,
    #         publish_timestamp=libs.tool.get_timestamp()
    #     ).where(phpmps_member_vip.user_name == self.uname)
    #     entry.execute()

    def get_coupon_last_timestamp(self):
        return (phpmps_member_vip.get(user_name=self.uname).coupon_last_timestamp)

    def get_remain_coupon_num(self):
        return (phpmps_member_vip.get(user_name=self.uname).coupon_num)

    def coupon_reset(self):
        entry = phpmps_member_vip.update(
            coupon_num=c.coupon_num_a_day,
            coupon_last_timestamp=libs.tool.get_timestamp()
        ).where(phpmps_member_vip.user_name == self.uname)
        entry.execute()

    def login_stamp_update(self):
        entry = phpmps_member_vip.update(
            login_timestamp=libs.tool.get_timestamp()
        ).where(phpmps_member_vip.user_name == self.uname)
        entry.execute()


    def coupon_num_decrease(self):
        tt = self.get_remain_coupon_num()
        if tt > 0:
            entry = phpmps_member_vip.update(
                coupon_num=tt - 1,
                coupon_last_timestamp=libs.tool.get_timestamp(),
            ).where(phpmps_member_vip.user_name == self.uname)
            entry.execute()

    def jifen_increase(self, num=1):
        # tt = self.get_by_username(u_name).def_jifen
        tt = phpmps_member_vip.get(user_name=self.uname).def_jifen
        entry = phpmps_member_vip.update(def_jifen=tt + num, ).where(phpmps_member_vip.user_name == self.uname)
        entry.execute()

    def get_by_username(self):
        try:
            return (phpmps_member_vip.get(user_name=self.uname))
        except:
            return None

    # def get_by_tel(self, tel):
    #     return (phpmps_member_vip.get(phone=tel))

    def get_by_parentid(self, cat_id):
        # print('>'* 80)
        # print(cat_id)
        try:
            return (phpmps_member_vip.get(
                (phpmps_member_vip.parentid == cat_id) &
                (phpmps_member_vip.user_name == self.uname)))
        except:
            return None

            # def update_touxiang(self, imagepath):
            #     try:
            #         entry = phpmps_member_vip.update(
            #             img_touxiang=imagepath,
            #         ).where(phpmps_member_vip.user_name == self.uname)
            #         entry.execute()
            #         return (True)
            #     except:
            #         return (False)

            # def charge(self, amount):
            #     jinbi = amount * c.rmb2jinbi + self.get_jinbi_num()
            #     entry = phpmps_member_vip.update(
            #         def_jinbi=jinbi,
            #     ).where(phpmps_member_vip.user_name == self.uname)
            #     entry.execute()
            #     return (True)
            #
            # def convert(self, amount):
            #     jifen = self.get_jifen_num() - amount * c.jinbi2jifen
            #     if jifen < 0:
            #         return False
            #     jinbi = self.get_jinbi_num() + amount
            #     entry = phpmps_member_vip.update(
            #         def_jinbi=jinbi,
            #         def_jifen=jifen,
            #     ).where(phpmps_member_vip.user_name == self.uname)
            #     entry.execute()
            #     return (True)

            # def buy_refresh(self, amount):
            #     current_jinbi = self.get_jinbi_num()
            #     if amount > current_jinbi:
            #         return False
            #     refresh_num = amount * c.jinbi2refresh + self.get_buy_refresh_num()
            #     entry = phpmps_member_vip.update(
            #         buy_refresh_num=refresh_num,
            #         def_jinbi=self.get_jinbi_num() - amount,
            #     ).where(phpmps_member_vip.user_name == self.uname)
            #     entry.execute()
            #     return (True)

            # def buy_publish(self, amount):
            #     current_jinbi = self.get_jinbi_num()
            #     if amount > current_jinbi:
            #         return False
            #     publish_num = amount * c.jinbi2publish + self.get_buy_publish_num()
            #     entry = phpmps_member_vip.update(
            #         buy_publish_num=publish_num,
            #         def_jinbi=self.get_jinbi_num() - amount,
            #     ).where(phpmps_member_vip.user_name == self.uname)
            #     entry.execute()
            #     return (True)
            #
            # def buy_zhiding(self, amount):
            #     current_jinbi = self.get_jinbi_num()
            #     if amount > current_jinbi:
            #         return False
            #     zhiding_num = amount * c.jinbi2zhiding + self.get_buy_zhiding_num()
            #     entry = phpmps_member_vip.update(
            #         buy_zhiding_num=zhiding_num,
            #         def_jinbi=self.get_jinbi_num() - amount,
            #     ).where(phpmps_member_vip.user_name == self.uname)
            #     entry.execute()
            #     return (True)

            # def update_password(self, new_password):
            #     try:
            #         entry = phpmps_member_vip.update(
            #             user_pass=libs.tool.md5(new_password),
            #         ).where(phpmps_member_vip.user_name == self.uname)
            #         entry.execute()
            #         return (True)
            #     except:
            #         return (False)
            #     return (False)
            #
            #
            # def update_userinfo(self, post_data):
            #     entry = phpmps_member_vip.update(
            #         email=post_data['email'][0],
            #         phone=post_data['tel'][0],
            #         cname=post_data['cname'][0],
            #         sex=post_data['sex'][0],
            #         qq=post_data['qq'][0]
            #     ).where(phpmps_member_vip.user_name == self.uname)
            #     entry.execute()

            # def update_coupon(self, info_dic):
            #     entry = phpmps_member_vip.update(
            #         coupon_uid=info_dic['coupon_uid'],
            #         coupon_timestamp=info_dic['coupon_timestamp'],
            #
            #     ).where(phpmps_member_vip.user_name == info_dic['userid'])
            #     entry.execute()
            #
            # def delete_user(self):
            #     query = phpmps_member_vip.delete().where(phpmps_member_vip.user_name == self.uname)
            #     query.execute()  # Returns the number of rows deleted.
            #
            #
            # def insert_data(self, post_data):
            #     entry = phpmps_member_vip.create(
            #         user_name=post_data['user_name'][0],
            #     )



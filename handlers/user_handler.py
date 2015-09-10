# -*- coding:utf-8 -*-
'''
会员后台管理
'''

import time

# from model.info_model import MInfo
# from model.member_model import MUser
# from model.city_model import MCity
from model.shoucang_model import MShoucang
import core.base_handler as base_handler
import libs.tool
import core.config


class UserHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()

        self.mshoucang = MShoucang()


    def get(self, input=''):

        if len(input) > 0:
            par_arr = input.split('/')
        if self.user_name is None or self.user_name == '':
            self.redirect('/member/login')
        self.reset_num()
        if input == '':
            self.get_main_page()
        elif input == 'get_user_info':
            self.get_user_head_info()
        elif input == 'page_published':
            self.page_published()
        elif input == 'page_contact':
            self.page_contact()
        elif input == 'p_status':
            self.page_status()
        elif input.startswith('p_coupon'):
            self.page_coupon()
        elif input == 'p_shoucang':
            self.view_shoucang()
        elif input == 'p_finance_charge':
            self.view_finance_charge()
        elif input == 'p_finance_buy_refresh':
            self.p_finance_buy_refresh()
        elif input == 'p_finance_buy_zhiding':
            self.p_finance_buy_zhiding()
        elif input.startswith('shoucang'):
            info_uid = input.split('/')[1]
            self.shoucang(info_uid)
        elif input.startswith('del_shoucang'):
            shoucang_id = input.split('/')[1]
            self.mshoucang.del_by_id(shoucang_id)
            self.view_shoucang()
        elif input.startswith('p_'):
            kwd = {
                'cityid': self.city_name,
                'cityname': self.mcity.get_cityname_by_id(self.city_name),
                'parentid': '0000',
                'parentlist': '',
            }
            self.render('tpl_user/{0}.html'.format(input),
                        kwd=kwd,
                        wuserinfo=self.muser_info.get_by_username(),
                        wusernum=self.muser_num.get_by_username(),
                        # wuservip=self.muser_vip.get_by_username(),
            )

        elif input.startswith('p_jianli'):
            self.view_jianli(input)
        else:
            self.set_status(400)
            self.render('404.html')

    def shoucang(self, info_uid):
        uid = libs.tool.md5(''.join([self.user_name, info_uid]))
        if self.mshoucang.has_record(uid):
            self.set_status(400)
        else:
            info_dic = {
                'uid': uid,
                'timestamp': libs.tool.get_timestamp(),
                'userid': self.user_name,
                'info_uid': info_uid,
                'catname': self.minfo.get_by_id(info_uid)['catname'],
                'title': self.minfo.get_by_id(info_uid)['title'][0],
            }
            try:
                self.mshoucang.insert_data(info_dic)
            except:
                self.set_status(200)

    def post(self, input=''):
        if input == 'changepass':
            self.changepass()
        elif input == 'touxiang':
            self.change_tuoxiang()
        elif input == 'updateinfo':
            self.update_user_info()
        elif input == 'renzheng':
            self.renzheng()
        else:
            self.redirect('/user/')

    def renzheng(self):
        # print('hello')
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        file_dict_list = self.request.files['imageName']
        for file_dict in file_dict_list:
            file_up_str = libs.upload.upload_imgfile(file_dict)
            break
        else:
            file_up_str = ''

        self.muser_info.update_renzheng(file_up_str)
        self.redirect('/user/p_renzheng')

    def update_user_info(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        if True == self.muser_info.update_userinfo(post_data):
            self.redirect('/user/')
        else:
            self.redirect('/user/')

    def page_coupon(self):
        self.render('tpl_user/p_coupon.html')

    def page_status(self):
        userinfo = self.muser_info.get_by_username()
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': '',
        }
        if userinfo.img_touxiang is None or userinfo.img_touxiang == '':
            userinfo.img_touxiang = 'fixed/touxiang.jpg'
        self.render('tpl_user/p_status.html',
                    kwd=kwd,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),

        )


    def view_shoucang(self):
        shoucang_info = self.mshoucang.get_by_userid(self.user_name)
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            # 'vip_cat': self.vip_cat,
        }
        self.render('tpl_user/p_shoucang.html',
                    kwd=kwd,
                    shoucang_info=shoucang_info,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),
                    )

    def p_finance_buy_refresh(self):
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': '',
            'username': self.user_name,
        }
        self.render('tpl_user/p_finance_buy_refresh.html',
                    kwd=kwd,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),

        )

    def p_finance_buy_zhiding(self):
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': '',
            'username': self.user_name,
        }
        self.render('tpl_user/p_finance_buy_zhiding.html',
                    kwd=kwd,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),

        )

    def view_jianli(self, input):
        tt = input.split('/')
        zhiwei_id = tt[1]
        zhiwei_info = self.minfo.get_by_id(zhiwei_id)
        self.render('tpl_user/p_jianli.html',
                    zhiwei_info=zhiwei_info,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),
                    )

    def page_contact(self):
        # userinfo = self.muser.get_by_username(self.user_name)
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': '',
        }
        self.render('tpl_user/page_contact.html',
                    kwd=kwd,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),

        )

    def change_tuoxiang(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        # 保存上传之后的图片的相对路径（static)
        file_up_str = ''

        file_dict_list = self.request.files['user_touiang']
        # 对上传的图片进行处理
        for file_dict in file_dict_list:
            # tools.markit()
            file_up_str = libs.upload.upload_imgfile(file_dict)
            break
        else:
            file_up_str = ''

        self.muser_info.update_touxiang(file_up_str)
        self.redirect('/user/')

    def reset_num(self):
        self.muser_num.reset_refresh_num()
        self.muser_num.reset_publish_num()
        # 不管是不是VIP，都初始化
        self.muser_vip.reset_refresh_num(self.muser_info.get_vip_cats())
        self.muser_vip.reset_publish_num(self.muser_info.get_vip_cats())
        self.muser_vip.reset_tuiguang_num(self.muser_info.get_vip_cats())
        self.muser_vip.reset_yuyue_num(self.muser_info.get_vip_cats())

        self.reset_coupon_num()


    def reset_coupon_num(self):
        # 根据最后刷新的日期判断，是否要重置刷新次数
        last_refresh_date = time.strftime("%Y-%m-%d", time.localtime(self.muser_info.get_coupon_last_timestamp()))
        current_date = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

        if (last_refresh_date != current_date):
            self.muser_info.coupon_reset()

    def get_main_page(self):

        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': '',
            'username': self.user_name,
        }
        self.render('tpl_user/index.html',

                    kwd=kwd,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),
                    )

    # Modified: 2014-12-21
    # def page_published(self):
    # userid = self.get_secure_cookie('login_user')


    def view_finance_charge(self):
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': '',
            'username': self.user_name,
        }
        self.render('tpl_user/p_finance_charge.html',
                    kwd=kwd,
                    wuserinfo=self.muser_info.get_by_username(),
                    wusernum=self.muser_num.get_by_username(),
                     )
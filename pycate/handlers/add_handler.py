# -*- coding:utf-8 -*-
'''
添加信息
'''

import uuid

import tornado.web

import libs
import core.base_handler as base_handler
from core.config import c
from pycate.model.catalog_model import MCatalog
from pycate.model.city_model import MCity


# from model.member_mode_l import MUser


class AddHandler(base_handler.PycateBaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        # self.minfo = MInfo(self.city_name)
        self.mcat = MCatalog()
        self.mcity = MCity()
        # self.muser_info = MUser(self.user_name)


    def get(self, input=''):
        url_arr = input.split('/')
        if len(input) == 4:
            self.toadd(input)
        elif len(url_arr[0]) == 4 and url_arr[1] == 'vip':
            self.toadd(url_arr[0], '1')
        else:
            self.render('404.html')

    def post(self, input=''):
        if len(input) > 0:
            self.add()

    @tornado.web.authenticated
    def toadd(self, catid, vip='0'):
        ip = self.request.remote_ip
        # if 'True' != self.get_secure_cookie(config.cookie_str['is_login']).decode('utf-8'):
        # self.redirect('/member/login')
        # userinfo = self.muser_info.get_by_username()
        uid = str(uuid.uuid1())
        kwd = {
            'uid': uid,
            'userid': self.user_name,
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'catid': catid,
            'parentid': catid[:2] + '00',
            'parentname': self.mcat.get_by_id(catid[:2] + '00').catname,
            'catname': self.mcat.get_by_id(catid).catname,
            'parentlist': self.mcat.get_parent_list(),
            'chenghu': '',
            'phone': '',
            'qq': '',
            'email': self.userinfo.user_email,
            'userip': ip,
            'vip': vip,
        }
        self.render('add/add_{0}.html'.format(catid), kwd=kwd)

    @tornado.web.authenticated
    def add(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        uid = post_data['uid'][0]
        # 对uid进行判断，防止反复发布同一信息。
        uu = self.minfo.get_by_id(uid)
        if str(uu) == 'None':
            pass
        else:
            self.render('not_repeat.html')
            return

        # 保存上传之后的图片的相对路径（ static )
        img_path_arr = []

        try:
            file_dict_list = self.request.files['mymps_img']
            for file_dict in file_dict_list:
                file_up_str = libs.upload.upload_imgfile(file_dict)
                img_path_arr.append(file_up_str)
        except:
            pass
        post_data['mymps_img'] = img_path_arr

        # 对面积进行处理
        if 'extra_mianji' in post_data:
            mianji_flt = float(post_data['extra_mianji'][0])
            if 'extra_mianji' in post_data:
                if mianji_flt < 20:
                    post_data['extra_mianji1'] = [1]
                elif mianji_flt < 40:
                    post_data['extra_mianji1'] = [2]
                elif mianji_flt < 60:
                    post_data['extra_mianji1'] = [3]
                elif mianji_flt < 90:
                    post_data['extra_mianji1'] = [4]
                elif mianji_flt < 120:
                    post_data['extra_mianji1'] = [5]
                elif mianji_flt < 200:
                    post_data['extra_mianji1'] = [6]
                elif mianji_flt >= 200:
                    post_data['extra_mianji1'] = [7]

        ts = libs.tool.get_timestamp()
        ts_str = libs.tool.get_time_str(ts)

        parentid = post_data['parentid'][0]
        post_data['catname'] = self.mcat.get_by_id(post_data['catid'][0]).catname
        post_data['userid'] = self.user_name
        post_data['views'] = 1
        post_data['create_time'] = ts
        post_data['update_time'] = ts

        ## 添加控制字段
        post_data['def_uid'] = str(uid)
        post_data['def_create_time_str'] = ts_str
        post_data['def_update_time_str'] = ts_str

        # 记录的超时的时间
        # 推广


        post_data['def_tuiguang_out_time'] = ts
        # 置顶
        post_data['def_zhiding'] = 0
        post_data['def_zhiding_out_time'] = ts
        # 刷新
        post_data['def_refresh'] = 1
        post_data['def_refresh_out_time'] = ts + c.refresh_timeout
        # 是否有效。是否通过审核
        post_data['def_valid'] = 1
        post_data['def_banned'] = 0

        if post_data['vip'][0] == '1':
            post_data['def_tuiguang'] = 1
            # print('>'* 80)
            # print(parentid)
            if self.muser_vip.get_vip_publish_num(parentid) <= 0:
                return False
            if self.__should_banned(post_data) == True:
                post_data['def_banned'] = 1
                if self.minfo.insert_data(post_data) == True:
                    self.muser_vip.publish_num_decrease(parentid)

                    self.render('banned.html')
                else:
                    self.render('error.html')
            else:
                if self.minfo.insert_data(post_data) == True:
                    self.muser_vip.publish_num_decrease(parentid)

                    self.muser_num.jifen_increase(num=2)
                    self.redirect('/list/{0}'.format(post_data['catid'][0]))
                else:
                    self.render('error.html')
        else:
            post_data['def_tuiguang'] = 0
            # if self.muser_num.get_free_publish_num() + self.muser_num.get_buy_publish_num() <= 0:
            #     return False
            if self.__should_banned(post_data) == True:
                post_data['def_banned'] = 1
                if self.minfo.insert_data(post_data) == True:
                    # self.muser_num.publish_num_decrease()
                    self.render('banned.html')
                else:
                    self.render('error.html')
            else:
                if self.minfo.insert_data(post_data) == True:
                    # self.muser_num.publish_num_decrease()
                    # self.muser_num.jifen_increase(num=2)
                    self.redirect('/list/{0}'.format(post_data['catid'][0]))
                else:
                    self.render('error.html')

    def __should_banned(self, post_data):
        if libs.dfa.filter.isContain(post_data['title'][0]) == True:
            return True
        if libs.dfa.filter.isContain(post_data['content'][0]) == True:
            return True
        return False



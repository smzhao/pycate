# -*- coding:utf-8 -*-
'''
一些形式单一的操作，针对用户的
'''
import tornado.web

from model.member_model_info import MUserInfo
from model.info_model import MInfo


class AdminOperateHandler(tornado.web.RequestHandler):
    def initialize(self, hinfo=''):
        self.cityid = self.get_secure_cookie('cityid').decode('utf-8')
        self.m_user = MUserInfo()
        self.minfo = MInfo(self.cityid)

    def get(self, input=''):
        # self.write(r'<h3>' + input + r'</h3>')
        if len(input) > 0:
            ip_arr = input.split(r'/')
            # self.render()
            if ip_arr[0] == 'vip':
                self.set_vip(ip_arr[1])
            elif ip_arr[0] == 'renzheng':
                self.set_credit(ip_arr[1])
            elif ip_arr[0] == 'valid':
                self.set_info_valid(ip_arr[1])
        else:
            self.render('404.html')

    def set_vip(self, def_uid):
        # print(def_uid)
        self.m_user.set_vip(def_uid)
        self.redirect('/admin/page_members')

    def set_credit(self, def_uid):
        # print(def_uid)
        self.m_user.set_credit(def_uid)
        self.redirect('/admin/page_members')

    def set_info_valid(self, info_uid):
        self.minfo.set_valid(info_uid)
        self.redirect('/admin/list/check')
        pass

# -*- coding:utf-8 -*-

import tornado.web
from model.catalog_model import MCatalog


class WidgetHandler(tornado.web.RequestHandler):
    def initialize(self, hinfo=''):
        self.mcat = MCatalog()

    def get(self, input=''):
        if input == 'loginfo':
            self.loginfo()

    def get_user_cookie(self):
        out_str = ''
        cookie = self.get_secure_cookie("user")
        if cookie == None:
            out_str = r'<a href="" title="用QQ帐号登录">用QQ登陆</a> &nbsp;|&nbsp;&nbsp;<a href=\"" >登录</a>&nbsp;&nbsp;<a href="" >注册</a>");'
        return (out_str)


    def loginfo(self):
        if self.get_secure_cookie("user"):
            self.render('widget/loginfo.html', username=self.get_secure_cookie("user"))
        else:
            self.render(('widget/tologinfo.html'))

# -*- coding:utf-8 -*-
'''
网站后台管理
'''
import tornado.web
from core import config

from model.info_model import MInfo
from model.member_model_admin import MAdminUser
from model.city_model import MCity
from model.catalog_model import MCatalog


class AdminHandler(tornado.web.RequestHandler):
    def initialize(self, hinfo=''):
        userid = self.get_secure_cookie('admin_user')
        if userid is None:
            self.userid = ''
        else:
            self.userid = userid.decode('utf-8')
        cityid = self.get_secure_cookie('cityid')
        if cityid is None:
            self.cityid = 'changchun'
            self.set_secure_cookie('cityid', 'changchun')
        else:
            self.cityid = cityid.decode('utf-8')
        self.madmin = MAdminUser()
        self.mcat = MCatalog()
        self.mcity = MCity()
        self.minfo = MInfo(self.cityid)


    def post(self, input=''):
        if input == '':
            # ip_arr = input.split(r'/')
            infos = self.request.arguments
            for x in infos:
                # self.write(str(x))
                pass
        elif input == 'user_set':
            self.set_vip()
        self.set_secure_cookie(config.cookie_str['admin_user'], 'admin')
        self.render('tpl_admin/main.html')

    def set_vip(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        if post_data['isvip'][0] == '1':
            self.madmin.set_vip(post_data['user_name'][0], post_data['cats'])
        else:
            self.madmin.cancel_vip(post_data['user_name'][0])

        self.redirect('/admin/userinfo/{0}'.format(post_data['user_name'][0]))

    def get(self, input=''):
        # self.write(r'<h3>' + input + r'</h3>')
        url_arr = input.split('/')
        if input == '':
            self.view_main()
        elif input == 'left':
            pass
        elif input == 'list_renzheng':
            self.list_renzheng()
        elif input == 'page_members':
            self.page_published()
        elif input.startswith('p_'):
            self.open_p(input)
        elif url_arr[0] == 'user':
            self.get_user_frame(url_arr[1])
        elif url_arr[0] == 'userinfo':
            self.get_user(url_arr[1])
        elif input.startswith('list/'):
            self.listinfo(input)
        else:
            pass
    def open_p(self, input):
        self.render('tpl_admin/%s.html' % (input))
    def get_user_frame(self, user_name):
        self.render('tpl_admin/p_user_toset_frame.html', user_name=user_name)
    def get_user(self, user_name):
        uinfo = self.madmin.get_by_username(user_name)
        clas = self.mcat.get_parent_list()
        vip_cat = uinfo.vip_cat
        if uinfo:
            self.render('tpl_admin/p_user_toset.html', uinfo=uinfo,  cats = clas, vip_cat=vip_cat)
        else:
            self.open_p('p_set_vip')

    def listinfo(self, input):
        # opter, cityid, sig = input.split('/')

        opter, switch = input.split('/')

        # cityid = input.split('_')[1]

        if switch == 'check':
            condition = {'def_valid': 0, 'def_banned': 0}
        # elif switch == 'tuiguang':
        # condition = {"catid": {"$in": self.vip_cat}, 'userid': self.userid}
        # elif switch == 'notg':
        #     condition = {"catid": {"$nin": self.vip_cat}, 'userid': self.userid}
        user_published_infos = self.minfo.get_by_condition(condition)
        kwd = {
            'cityid': self.cityid,
            'cityname': self.mcity.get_cityname_by_id(self.cityid),
            'action': switch
        }
        self.render('tpl_admin/p_listcity.html', user_published_infos=user_published_infos, kwd=kwd)

    def get_top_page(self):
        m_user = self.muser.get_by_username()
        self.render('tpl_admin/top.html', username=self.userid, userinfo=m_user)

    def page_published(self):
        if self.userid != '':
            user_recs = self.muser.get_all()
            out_str = '<ul>'
            for user_rec in user_recs:
                tmp_str = '<li>{0}</li>'.format(user_rec.user_name)
                out_str += tmp_str
            out_str += '</ul'
            return out_str

        else:
            self.render('tpl_admin/index.html')


    def list_renzheng(self):
        if self.userid != '':
            user_recs = self.madmin.get_uncredit()
            for u in user_recs:
                print (u.user_name)
            self.render('tpl_admin/p_members.html',
                        wuser_recs = user_recs)

        else:
            self.render('tpl_admin/index.html')

    def view_main(self):
        if self.userid == '':
            self.render('tpl_admin/index.html')
        else:
            self.render('tpl_admin/main.html')


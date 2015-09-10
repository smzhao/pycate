# -*- coding:utf-8 -*-

import libs.upload
import tornado.web

# from model.info_model import MInfo
from model.catalog_model import MCatalog
from model.link_model import MLink
from model.member_model import MUser
from model.city_model import MCity
import core.base_handler as base_handler

class LinkHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.mlink = MLink()
        self.mcat = MCatalog()
        self.muser_info = MUser(self.user_name)
        self.mcity = MCity()
        vip_cat = self.muser_info.get_by_username().vip_cat.strip().split(',')
        if vip_cat == ['']:
            self.vip_cat = []
        else:
            self.vip_cat = vip_cat

    def get(self, input=''):
        # Todo: 验证
        if input == 'add':
            self.to_add()
        elif input == 'list':
            self.list()
        elif input.startswith('delete'):
            self.delete_by_id(input)
        elif input.startswith('edit'):
            self.to_edit(input)
        else:
            op, catid = input.split(r'/')
            if op == 'get_list':
                self.get_list()

    @tornado.web.authenticated
    def delete_by_id(self, input):
        op, uid = input.split('/')
        self.mlink.delete_by_uid(uid)
        self.list()


    def post(self, input=''):
        if input == 'add':
            self.add()
        elif input.startswith('edit'):
            self.update()

    @tornado.web.authenticated
    def add(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        file_dict = self.request.files['link_image'][0]
        # 对上传的图片进行处理
        file_up_str = libs.upload.upload_imgfile(file_dict)
        out_arr = {'img': file_up_str}
        out_arr['url'] = post_data['link_url'][0]
        out_arr['catid'] = post_data['catid'][0]
        out_arr['cityid'] = self.city_name
        out_arr['parentid'] = post_data['catid'][0][:2] + '00'
        out_arr['username'] = self.user_name
        self.mlink.insert_rec(out_arr)
        self.redirect('/link/list')


    def update(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        if 'elink_image' in self.request.files:
            file_dict = self.request.files['elink_image'][0]
            file_up_str = libs.upload.upload_imgfile(file_dict)
            out_arr = {'img': file_up_str}
        else:
            out_arr = {'img': post_data['old_img'][0]}

        out_arr['url'] = post_data['elink_url'][0]
        out_arr['catid'] = post_data['ecatid'][0]
        self.mlink.update(post_data['uid'][0], out_arr)
        self.redirect('/link/list')


    def list(self):

        cat_str = '''<option value='' selected >请选择</option>'''
        for cat_id in self.vip_cat:
            cat_name = self.mcat.get_by_id(cat_id).catname
            tmp_str = '''<option value="%s" >%s</option>''' % (cat_id, cat_name)
            cat_str += tmp_str



        infos = self.mlink.get_links_by_cityid(self.user_name,self.city_name)
        kwd = {
            'userid': self.user_name,
            'cityname': '',
            'cityid': self.city_name,
            'cat_str': cat_str,
            'parentid': '0000',
            'parentlist': self.mcat.get_parent_list(),

        }

        self.render('link/list.html', infos=infos,  kwd=kwd,  userinfo=self.muser_info.get_by_username())

    def to_add(self):
        cat_str = '''<option value='' selected >请选择</option>'''
        for cat_id in self.vip_cat:
            cat_name = self.mcat.get_by_id(cat_id).catname
            tmp_str = '''<option value="%s" >%s</option>''' % (cat_id, cat_name)
            cat_str += tmp_str


        kwd = {
            'userid': self.user_name,
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'cat_str': cat_str,
            'parentid': '0000',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('link/list.html', kwd=kwd)


    def to_edit(self, input):
        op, uid = input.split('/')
        linkinfo = self.mlink.get_by_id(uid)
        tmp_s1 = ''
        tmp_s2 = ''
        tmp_s3 = ''
        link_cityid = linkinfo.cityid.strip()
        if link_cityid == 'changchun':
            tmp_s1 = 'selected'
        elif link_cityid == 'tonghua':
            tmp_s2 = 'selected'
        elif link_cityid == 'jilin':
            tmp_s3 = 'selected'



        cat_str = '''<option value='' selected >请选择</option>
        '''
        for cat_id in self.vip_cat:
            cat_name = self.mcat.get_by_id(cat_id).catname
            tmp_str_jcc = ''
            if cat_id == linkinfo.catid:
                tmp_str_jcc = 'selected=selected'
            tmp_str = '''<option value="{0}" {1}>{2}</option>'''.format(cat_id, tmp_str_jcc, cat_name)
            cat_str += tmp_str

        kwd = {
            'userid': self.user_name,
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'cat_str': cat_str,
            'parentid': '0000',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('link/list.html', kwd=kwd, linkinfo=linkinfo)
# -*- coding:utf-8 -*-
'''
一些形式单一的操作
'''

from core.base_handler import BaseHandler
from model.link_model import MLink
from model.catalog_model import MCatalog
import libs


class DocumentHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.mlink = MLink(self.city_name)
        self.mcat = MCatalog()
        # self.muser_info = MUser(self.user_name)


        # self.mcat = MCatalog()
        # self.mcity = MCity()

    def get(self, url_str=''):
        tmp_uu = url_str.split(r'/')
        kwd = {
            'cityname': self.city_name,
            'parentid': '0000',
            'parentlist': ['1 ','2'],
        }
        if len(tmp_uu) == 1:
            self.view_document(url_str)
        else:
            self.render('404.html')

    def view_document(self, html_name):
        bread_crumb_nav_str = '<li>当前位置： </li><li><a href="/">吉合营</a></li>'
        bread_crumb_nav_str += '<li> > </li>'

        link_recs = self.mlink.query_links_by_parentid('0100')
        out_link_str = libs.core.get_out_link_str(link_recs, self.static_url)

        parent_id = '0000'
        condition=''
        sub_menu_str = ''
        catname = ''
        num = 0
        kwd = {
            'catid': html_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'daohangstr': bread_crumb_nav_str,
            'linkstr': out_link_str,
            'parentid': parent_id,
            'parentlist': self.mcat.get_parent_list(),
            'condition': condition,
            'sub_menu': sub_menu_str,
            'catname': catname,
            'rec_num': num,
        }
        self.render('document/{0}'.format(html_name), kwd=kwd)








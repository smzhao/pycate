# -*- coding:utf-8 -*-

import tornado

from core.config import c
from pycate.model.info_model import MInfo
from pycate.model.link_model import MLink
from pycate.model.catalog_model import MCatalog
from pycate.model.city_model import MCity
import libs
import core.base_handler as base_handler


class SearchHandler(base_handler.PycateBaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.minfo = MInfo(self.city_name)
        self.mcat = MCatalog()
        self.mlink = MLink()
        self.mcity = MCity()
        # self.muser_info = MUser(self.user_name)

    def get(self, input=''):
        kw = (tornado.escape.url_unescape(self.get_cookie('search_keyword')))
        if input == '':
            # 注释掉的为使用数据库存储
            # self.search(self.muser.get_last_keyword())
            self.search(kw)
        elif len(input) > 0:
            # 注释掉的为使用数据库存储
            # self.search(self.muser.get_last_keyword(), int(input))
            self.search(kw, int(input))
        else:
            self.write('Hello')

    # Todo: 可以使用Tornado处理
    def post(self, input=''):
        if self.user_name == '':
            self.render('search_login.html')
            return
        if input == '':
            keywords = self.get_argument('searchheader')
            '''
            其实这是因为文字编码而造成的，汉字是两个编码，所以才会搞出这么个乱码出来！
            其实解决的方法很简单：只要在写入Cookie时，先将其用Url编码，然后再写入，当我们读取时再解码就OK了，
            '''
            self.set_cookie('search_keyword', tornado.escape.url_escape(keywords))
            # 下面是使用数据库存储
            # self.muser.set_last_keyword(keywords)
            self.search(keywords)

    def search(self, kw, current=1):
        # Todo: 限定在当前分类
        bread_crumb_nav_str = '<li>当前位置： </li><li><a href="/">吉合营</a></li>'
        condition = {'title': {"$regex": kw}}

        condition['def_banned'] = 0
        condition['def_valid'] = 1
        condition['def_refresh'] = 1
        record_num = self.minfo.get_by_condition(condition).count()
        page_num = int(record_num / c.info_list_per_page) + 1
        cat_slug = 'search'
        kwd = {
            'imgname': 'fixed/zhanwei.png',
            'catid': input,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'daohangstr': bread_crumb_nav_str,
            'linkstr': '',
            'parentid': '0000',
            'parentlist': '',
            'condition': condition,
            'sub_menu': '',
            'catname': '',
            'rec_num': record_num,
            'pager': libs.tool.gen_pager(cat_slug, page_num, current)
        }
        dbdata = self.minfo.get_list_fenye(condition, current)
        self.render('search/list_res.html', kwd=kwd, info_list=dbdata)

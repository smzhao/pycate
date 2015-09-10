# -*- coding:utf-8 -*-
import math

from core import config
from core.config import c
from model.info_model import MInfo
from model.catalog_model import MCatalog
from model.link_model import MLink
from model.city_model import MCity
import core.base_handler as base_handler
import libs.tool
import libs.core


class ListHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.minfo = MInfo(self.city_name)
        self.mcat = MCatalog()
        self.mlink = MLink(self.city_name)
        self.mcity = MCity()

    def get(self, input=''):
        if len(input) == 4:
            self.list(input)
        # elif input == 'search':
        #     keywords = self.request.arguments['keywords'][0]
        #     self.search(keywords)
        elif len(input) > 4:
            # 如果带条件传回
            self.echo_html(input)
        else:
            self.render('404.html')

    # 2014-12-20
    #   def post(self, input=''):
    #       pass
    #       # print('*' * 20)
    #       # if len(input) > 0:
    #     #     self.add()

    def echo_html(self, input):
        input_arr = input.split('/')

        pa_arr = input.split('/')
        sig = pa_arr[0]

        num = (len(pa_arr) - 2) // 2

        # 包装成条件字典# condition 为用于查询的条件. 字典

        if sig.endswith('00'):
            condition = {'parentid': sig}
        else:
            condition = {'catid': sig}
        fenye_num = 1
        for ii in range(num):
            ckey = pa_arr[ii * 2 + 2]

            tval = pa_arr[ii * 2 + 3]
            if tval == '0':
                continue
            if ckey == 'fenye':
                # 分页参数。单独处理。
                fenye_num = int(tval)
                continue
            if ckey == 'fabiaoshijian':
                if tval == '1':
                    cval = 1
                elif tval == '2':
                    cval = 2
            else:
                cval = tval
            ckey = 'extra_' + ckey
            condition[ckey] = cval

        # 有效的条件
        condition['def_banned'] = 0
        condition['def_valid'] = 1

        print(condition)

        if input_arr[1] == 'con':
            infos = self.minfo.get_list_fenye(condition, fenye_num)
            for x in infos:
                for y in x:
                    print(y)
            self.echo_html_list_str(infos)
        elif input_arr[1] == 'num':
            allinfos = self.minfo.get_list(condition)
            self.echo_html_fenye_str(len(allinfos), fenye_num)

    def echo_html_list_str(self, infos):
        '''
        生成 list 后的 HTML 格式的字符串
        '''
        outstr = ''

        for info in infos:

            zhiding_str = ''
            tuiguang_str = ''
            imgname = 'fixed/zhanwei.png'
            if len(info['mymps_img']) > 0:
                imgname = info['mymps_img'][0]
            # print(imgname)
            if info['def_zhiding'] == 1:
                zhiding_str = '<span class="red">（已置顶）</span>'
            if info['def_tuiguang'] == 1:
                tuiguang_str = '<span class="red">（已推广）</span>'

            list_type = info['catid'][0]

            html_top_str = ''
            if 'extra_fangjia' in info:
                html_top_str = '''
                房价： <span class="red">{0}</span>
                '''.format(info['extra_fangjia'][0])
            html_bottom_str = ''

            kwd = {
                'imgname': imgname,
                'zhiding': zhiding_str,
                'tuiguang': tuiguang_str,
                'html_right_top': html_top_str,
                'html_right_bottom': html_bottom_str,
            }

            outstr += self.render_string('infolist/infolist_{0}.html'.format(list_type),
                                         kwd=kwd, post_info=info,
                                         widget_info = kwd).decode('utf-8')

        self.write(outstr)

    def echo_html_fenye_str(self, rec_num, fenye_num):
        '''
        生成分页的导航
        '''
        pagination_num = int(math.ceil(rec_num * 1.0 / c.info_list_per_page))

        if pagination_num == 1 or pagination_num == 0:
            # 只有一页时，不出现。
            fenye_str = ''
        elif pagination_num > 1:
            fenye_str = '<ul class="iga_pagination">'
            for num in range(1, pagination_num + 1):
                if num == fenye_num:
                    checkstr = 'active'
                else:
                    checkstr = 'disable'
                tmp_str_df = '''
                  <li class='{0}' name='fenye' onclick='change(this);'
                  value='{1}'><a>{1}</a></li>'''.format(checkstr, num)
                fenye_str += tmp_str_df
            fenye_str += '</ul>'

        else:
            pass
        self.write(fenye_str)


    def list(self, input):
        '''
        页面打开后的渲染方法，不包含 list 的查询结果与分页导航
        '''
        sig = input

        # 面包屑导航
        bread_crumb_nav_str = '当前位置：<a href="/">数据中心</a>'
        bread_crumb_nav_str += ' > '
        if input.endswith('00'):
            #　在打开一级类的情况下
            parent_id = input
            parent_catname = self.mcat.get_by_id(parent_id).catname
            condition = {'parentid': parent_id}
            catname = self.mcat.get_by_id(sig).catname
            bread_crumb_nav_str += '<a href="/list/{0}">{1}</a>'.format(sig, catname)

        else:
            # 在list 二级类的情况下
            condition = {'catid': sig}
            parent_id = sig[:2] + '00'
            parent_catname = self.mcat.get_by_id(parent_id).catname
            catname = self.mcat.get_by_id(sig).catname
            bread_crumb_nav_str += '<a href="/list/{0}">{1}</a>'.format(parent_id, parent_catname)
            bread_crumb_nav_str += ' > '
            bread_crumb_nav_str += '<a href="/list/{0}">{1}</a>'.format(sig, catname)
        # 右侧图片广告
        link_recs = self.mlink.query_links_by_parentid(parent_id)
        out_link_str = libs.core.get_out_link_str(link_recs, self.static_url)
        # 有效的条件
        condition['def_banned'] = 0
        condition['def_valid'] = 1
        condition['def_refresh'] = 1

        num = self.minfo.get_num_condition(condition)
        # 左侧二级菜单
        rnage2_list = self.mcat.get_range2_without_parent(parent_id)
        sub_menu_str = libs.core.get_sub_menu_str(rnage2_list, parent_catname)

        kwd = {
            'catid': input,
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
        self.render('list/list_{0}.html'.format(input), kwd=kwd, widget_info = kwd,)


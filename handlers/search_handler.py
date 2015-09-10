# -*- coding:utf-8 -*-

import math

import tornado
from core import config
from core.config import c
from model.info_model import MInfo
from model.link_model import MLink
from model.catalog_model import MCatalog
from model.city_model import MCity
from model.member_model_info import MUserInfo
import libs
import core.base_handler as base_handler


class SearchHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.minfo = MInfo(self.city_name)
        self.mcat = MCatalog()
        self.mlink = MLink()
        self.mcity = MCity()
        self.muser_info = MUser(self.user_name)

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
        # def echo_html(self, input):
        # kw = self.muser.get_last_keyword()
        # condition = {'title': {"$regex": kw}}
        # tmp = input.split('/')
        #
        # pa_arr = input.split('/')
        #     sig = pa_arr[0]
        #
        #     num = (len(pa_arr) - 2) // 2
        #
        #     # 包装成条件字典
        #     # condition 为用于查询的条件. 字典
        #
        #     fenye_num = 1
        #     for ii in range(num):
        #         ckey = pa_arr[ii * 2 + 2]
        #         tval = pa_arr[ii * 2 + 3]
        #         if tval == '0':
        #             continue
        #         if ckey == 'fenye':
        #             # 分页参数。单独处理。
        #             fenye_num = int(tval)
        #             continue
        #         if ckey == 'fabiaoshijian':
        #             if tval == '1':
        #                 cval = 1
        #             elif tval == '2':
        #                 cval = 2
        #         else:
        #             cval = tval
        #         ckey = 'extra_' + ckey
        #         condition[ckey] = cval
        #
        #     # 有效的条件
        #     condition['def_banned'] = 0
        #     condition['def_valid'] = 1
        #     infos = self.minfo.get_list_fenye(condition, fenye_num)
        #
        #     if tmp[1] == 'con':
        #         self.echo_html_list_str(infos)
        #     elif tmp[1] == 'num':
        #         allinfos = self.minfo.get_list(condition)
        #         self.echo_html_fenye_str(len(allinfos), fenye_num)

        # def echo_html_fenye_str(self, rec_num, fenye_num):
        #     '''
        #     生成分页的导航
        #     '''
        #     # 页面的数目
        #     input = int(math.ceil(rec_num * 1.0 / c.info_list_per_page))
        #
        #     if input == 1 or input == 0:
        #         # 只有一页时，不出现。
        #         fenye_str = ''
        #     elif input > 1:
        #         fenye_str = '<ul class="pagination">'
        #         for num in range(1, input + 1):
        #             if num == fenye_num:
        #                 checkstr = 'active'
        #             else:
        #                 checkstr = 'disable'
        #             tmp_str_df = '''
        #               <li class='{0}' name='fenye' onclick='change(this);'
        #               value='{1}'><a>{1}</a></li>'''.format(checkstr, num)
        #             fenye_str += tmp_str_df
        #         fenye_str += '</ul>'
        #
        #     else:
        #         return
        #     self.write(fenye_str)

        # def echo_html_list_str(self, infos):
        #     '''
        #     生成 list 后的 HTML 格式的字符串
        #     '''
        #     outstr = ''
        #     # uu = InfoList
        #     for info in infos:
        #         # outstr  += uu.renderit(info=info)
        #
        #         zhiding_str = ''
        #         tuiguang_str = ''
        #         imgname = 'fixed/zhanwei.png'
        #         if len(info['mymps_img']) > 0:
        #             imgname = info['mymps_img'][0]
        #         # print(imgname)
        #         if info['def_zhiding'] == 1:
        #             zhiding_str = '<span class="red">（已置顶）</span>'
        #         if info['def_tuiguang'] == 1:
        #             tuiguang_str = '<span class="red">（已推广）</span>'
        #
        #         list_type = info['catid'][0]
        #
        #         html_top_str = ''
        #         if 'extra_fangjia' in info:
        #             html_top_str = '''
        #             房价： <span class="red">{0}</span>
        #             '''.format(info['extra_fangjia'][0])
        #         html_bottom_str = ''
        #
        #         kwd = {
        #             'imgname': imgname,
        #             'zhiding': zhiding_str,
        #             'tuiguan': tuiguang_str,
        #             'html_right_top': html_top_str,
        #             'html_right_bottom': html_bottom_str,
        #         }
        #         outstr += self.render_string('infolist/infolist_{0}.html'.format(list_type),
        #                                      kwd=kwd, post_info=info).decode('utf-8')
        #     self.write(outstr)

        # def get_out_str(self, infos):
        #     '''
        #     更好的方式，是放到模板中 ?
        #     '''
        #     outstr = ''
        #     switcher = False
        #     for info in infos:
        #         style_str = ''
        #         zhiding_str = ''
        #         tuiguang_str = ''
        #         if switcher == True:
        #             switcher = False
        #             class_str = 'hover_odd'
        #         else:
        #             switcher = True
        #             class_str = 'hover_even'
        #         imgname = ''
        #         if len(info['mymps_img']) > 0:
        #             imgname = info['mymps_img'][0]
        #         if info['def_zhiding'] == 1:
        #             zhiding_str = '<span style="color:red;">（已置顶）</span>'
        #         if info['def_tuiguang'] == 1:
        #             tuiguang_str = '<span style="color:red;">（已推广）</span>'
        #         title_str = ' '.join([info['title'][0], zhiding_str, tuiguang_str])
        #
        #         outstr += '''<div class="{str_class}" >
        #         <span class="ltitlevalue">
        #         <a href="/view/{str_infoid}" target="_blank" style=" ">
        #         <font size=2 >{str_title}</font></a>
        #         <font class="area"></font> <span class="ltitle">
        #         <font size=2 style="font-family:Microsoft YaHei">
        #         <li size=3>
        #         <nobr> {str_content} </nobr>
        #         </li>
        #         <br/><br/>
        #         发布时间: {str_time}
        #         <span></span>
        #         </font></span></span>
        #         </BR>
        #         <span class="ltime"><font color=red size=3><b></b></font></span>
        #         </div>
        #         '''.format(str_class=class_str, str_infoid=info['def_uid'], str_img=self.static_url(imgname),
        #                    str_title=title_str, str_content=info['content'][0], str_time=info['def_update_time_str'])
        #
        #     return (outstr)
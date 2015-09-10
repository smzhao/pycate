# -*- coding:utf-8 -*-

import libs.tool
import libs.core
from model.info_model import MInfo
from model.catalog_model import MCatalog
from model.link_model import MLink
from model.city_model import MCity

import core.base_handler as base_handler
# from model.user_model import MUser

class InfoHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):
        # self.userid = self.get_secure_cookie('login_user').decode('utf-8')
        self.init_condition()
        self.mlink = MLink(self.city_name)
        self.mcat = MCatalog()


    def get(self, input=''):
        if len(input) == 36:
            self.view(input)
        elif input.startswith('shoucang'):
            info_uid = input.split('/')[1]
            self.shoucang(info_uid)
        else:
            self.render('404.html')

    def shoucang(self, info_uid):

        uid = libs.tool.md5(''.join([self.user_name, info_uid]))
        if self.mshoucang.has_record(uid):
            return
        info_dic = {
            'uid': uid,
            'timestamp': libs.tool.get_timestamp(),
            'userid': self.user_name,
            'info_uid': info_uid,
            'catname': self.minfo.get_by_id(info_uid)['catname'],
            'title': self.minfo.get_by_id(info_uid)['title'][0],
        }
        self.mshoucang.insert_data(info_dic)

    def post(self, input=''):
        self.update_jianli(input)


    def update_jianli(self, input):
        # print(input)
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        # for x in post_data:
        # print(post_data[x])
        self.minfo.update_jianli(input, post_data['jianli'][0])
        self.view(input)


    def is_viewable(self, info):


        if info['userid'] == self.user_name:
            # 如果是用户自己的，当然可以查看
            return True
        if info['def_valid'] != 1:
            return (False)
        if info['def_banned'] == 1:
            return (False)
        return True


    def view(self, uuid):
        info = self.minfo.get_by_id(uuid)
        if info is None:
            # 如果资源不存在
            self.set_status(404)
            self.render('404_view.html')
            return (False)
        elif self.is_viewable(info):
            pass
        else:
            self.render('404.html')
            return

        cat_id = info['catid'][0]
        parent_id = cat_id[:2] + '00'
        parent_catname = self.mcat.get_by_id(parent_id).catname
        catname = self.mcat.get_by_id(cat_id).catname

        daohang_str = '<a href="/">数据中心</a>'
        daohang_str += ' &gt; <a href="/list/{0}">{1}</a>'.format(parent_id, parent_catname)
        daohang_str += ' &gt; <a href="/list/{0}">{1}</a>'.format(cat_id, catname)

        ts = info['def_update_time_str']
        imgname = ''
        has_image = 0
        img_url = ''
        if len(info['mymps_img']) > 0:
            imgname = info['mymps_img'][0]
            has_image = 1
            img_url = self.static_url(imgname)
        # 左侧菜单
        rnage2_list = self.mcat.get_range2_without_parent(parent_id)
        sub_menu_str = libs.core.get_sub_menu_str(rnage2_list, parent_catname)
        # 右侧图片广告
        link_recs = self.mlink.get_links_by_catid(cat_id)
        out_link_str = libs.core.get_out_link_str(link_recs, self.static_url)

        # 自己发布的内容，不用收藏。

        if self.user_name == info['userid']:
           #  operate_str = '''<div id="g_fy" ><a href="/edit/{0}">编辑</a>
           #  <a href="/tuiguang/{0}" >推广</a>
           # <a href="/zhiding/{0}" >置顶</a>
           #  </div>
           #  '''.format(uuid)
           operate_str = ''


        else:
            operate_str = '''<span><a onclick="js_show_page('/user/shoucang/{0}')">收藏</a></span>'''.format(uuid)

        # 在DIV中的个人简历


        jianli_str = ''
        if parent_id == '0700':
            jianli_str = self.gen_jianli_str()

        kwd = {
            'img_url': img_url,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'timeit': ts,
            'daohangstr': daohang_str,
            'has_image': has_image,
            'parentid': parent_id,
            'parentlist': self.mcat.get_parent_list(),
            'sub_menu': sub_menu_str,
            'linkstr': out_link_str,
            'oprt_str': operate_str,
            'jianli_str': jianli_str,
            # 'maskip': maskip,
        }
        self.update_info_when_view(info)
        self.render('view/view_%s.html' % (info['catid'][0]), kwd=kwd, post_info=info)

    def gen_jianli_str(self):
        # 查看页面时，根据用户的信息，生成简历。
        tmp1_tou = '''
            <div id='inline_content' style='padding:10px; background:#fff; border: 2px solid #000088'>
            <form action='' method="post" >
            <legend>请选择使用哪份简历</legend>
             '''
        jianlis = self.minfo.get_user_jianli(self.user_name)

        if jianlis.count() == 0:
            tmp1_tou += '''
            <p>目前没有求职简历</p>
            <a href="/publish/0700">创建求职简历 </a>
            </div>
            '''
        else:
            # 第一次为 checked
            check_str = 'checked'
            for jianli in jianlis:
                tmp1_uuvv = '''<label>简历</label><input type="radio" {2} name="jianli" value="{0}" >{1} <br />
                '''.format(jianli['def_uid'], jianli['title'][0], check_str)
                check_str = ''
                tmp1_tou += tmp1_uuvv
            tmp1_tou += '''<button type="submit" class="ajax pure-button pure-button-primary" >确定</button></p>
                    </form></div>
                    '''

        # tmp1_tou += tmp1_hou
        return (tmp1_tou)

    def update_info_when_view(self, info):
        uuid = info['def_uid']
        self.minfo.update_view_count(uuid)
        # 根据时间判断，如果超时，则取消对应的权限
        timestamp = libs.tool.get_timestamp()
        if timestamp > info['def_tuiguang_out_time']:
            print('a')
            self.minfo.dis_tuiguang(uuid)
        if timestamp > info['def_zhiding_out_time']:
            print('b')
            self.minfo.dis_zhiding(uuid)
        if timestamp > info['def_refresh_out_time']:
            print('c')
            self.minfo.dis_fresh(uuid)



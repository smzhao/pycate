# -*- coding:utf-8 -*-

import libs.tool
import libs.core
from pycate.model.catalog_model import MCatalog
from pycate.model.link_model import MLink

import core.base_handler as base_handler
# from model.user_model import MUser

class InfoHandler(base_handler.PycateBaseHandler):
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
        # self.update_info_when_view(info)
        self.render('view/view_%s.html' % (info['catid'][0]), kwd=kwd, post_info=info)


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



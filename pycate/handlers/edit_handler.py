# -*- coding:utf-8 -*-
from core import config

import libs.tool
import libs.dfa
import libs.upload

from pycate.model.info_model import MInfo

from pycate.model.catalog_model import MCatalog
from pycate.model.city_model import MCity
import core.base_handler as base_handler

class EditHandler(base_handler.PycateBaseHandler):
    def initialize(self, hinfo=''):

        self.init_condition()


        self.minfo = MInfo(self.city_name)
        self.mcat = MCatalog()
        self.mcity = MCity()

    def get(self, input=''):
        if len(input) == 36:
            inf = self.minfo.get_by_id(input)
            if inf is None:
                self.render('404.html')
                return
            self.toedit(input)
        else:
            self.render('404.html')

    def post(self, input=''):
        if len(input) == 36:
            self.update(input)

    def is_editable(self, info):
        '''
        谁发布的谁编辑
        '''
        if info['userid'] == self.user_name:
            return True
        return False


    def toedit(self, infoid):
        rec_info = self.minfo.get_by_id(infoid)
        if self.is_editable(rec_info):
            pass
        else:
            return
        catid = rec_info['catid'][0]

        kwd = {
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'catid': catid,
            'parentid': catid[:2] + '00',
            'parentname': self.mcat.get_by_id(catid[:2] + '00').catname,
            'catname': self.mcat.get_by_id(catid).catname,
            'parentlist': self.mcat.get_parent_list(),

        }
        self.render('edit/edit_{0}.html'.format(catid), kwd=kwd, post_info=rec_info)

    def update(self, par_uid):
        post_data = self.minfo.get_by_id(par_uid)
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)


        img_path_arr = []

        try:
            file_dict_list = self.request.files['mymps_img']
            for file_dict in file_dict_list:
                file_up_str = libs.upload.upload_imgfile(file_dict)
                img_path_arr.append(file_up_str)
        except:
            pass
        post_data['mymps_img'] = img_path_arr
        # 对面积进行处理
        if 'extra_mianji' in post_data:
            mianji_flt = float(post_data['extra_mianji'][0])
            if 'extra_mianji' in post_data:
                if mianji_flt < 20:
                    post_data['extra_mianji1'] = [1]
                elif mianji_flt < 40:
                    post_data['extra_mianji1'] = [2]
                elif mianji_flt < 60:
                    post_data['extra_mianji1'] = [3]
                elif mianji_flt < 90:
                    post_data['extra_mianji1'] = [4]
                elif mianji_flt < 120:
                    post_data['extra_mianji1'] = [5]
                elif mianji_flt < 200:
                    post_data['extra_mianji1'] = [6]
                elif mianji_flt >= 200:
                    post_data['extra_mianji1'] = [7]
        # self.write("finish")

        ts = libs.tool.get_timestamp()
        ts_str = libs.tool.get_time_str(ts)

        post_data['catname'] = self.mcat.get_by_id(post_data['catid'][0]).catname

        # Save in pg database.
        # infoid_data = {'info_uid': uid}
        post_data['userid'] = self.user_name
        post_data['def_uid'] = str(par_uid)
        post_data['update_time'] = ts
        post_data['def_update_time_str'] = ts_str

        # infoid_data['zhiding_out_time'] = ts
        # 刷新
        post_data['def_refresh'] = 1
        post_data['def_refresh_out_time'] = ts + config.c.refresh_timeout
        # 是否有效。是否通过审核
        # 需要重新审核
        post_data['def_valid'] = 1
        post_data['def_banned'] = 0
        udi = self.minfo.update(par_uid, post_data)
        if libs.dfa.filter.isContain(post_data['title'][0]):
            post_data['def_banned'] = 1
            self.render('banned.html')
        self.redirect('/list/{0}'.format(post_data['catid'][0]))










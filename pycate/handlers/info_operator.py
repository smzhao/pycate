# -*- coding:utf-8 -*-
'''
一些形式单一的操作
'''
import datetime
import time

from core import config
import libs
from pycate.model.catalog_model import MCatalog
from pycate.model.refresh_model import MRefresh
import core.base_handler as base_handler


class OpHandler(base_handler.PycateBaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.mrefresh = MRefresh()
        self.mcat = MCatalog()


    def op_redirect(self, input):
        '''

        '''
        tmp_uu = input.split(r'/')
        uid = tmp_uu[0]
        action = tmp_uu[1]
        if len(tmp_uu) == 3:
            re_str = '''/tui/{0}/{1}'''.format(tmp_uu[2], action)
        else:
            re_str = '''/filter/{0}'''.format(action)

        self.redirect(re_str)

    def active_info(self, def_uid, sig):
        '''
        switch the status.
        用于刷新、推广、置顶
        '''
        info_dic = self.minfo.get_by_id(def_uid)
        # 值大，则权重高。
        weight = self.mcat.get_weight_id(info_dic['catid'][0])
        sigit = 'def_' + sig
        if info_dic[sigit] == 0:
            # 避免已经进行过操作
            info_dic[sigit] = 1
            sig_time = 'def_' + sig + '_out_time'
            timestamp = libs.tool.get_timestamp() + int(config.timeout[sig] / weight)
            info_dic[sig_time] = timestamp
            # 首先保证更新成功
            if self.minfo.update(def_uid, info_dic) == True:
                return True


    def update_userinfo(self, sig, parentid=''):
        if parentid == '':
            self.muser_num.num_decrease(sig)
        else:
            self.muser_vip.num_decrease(sig, parentid)


# class AppointHandler(OpHandler):
#     def post(self, input=''):
#         # print(input)
#         post_data = {}
#         for key in self.request.arguments:
#             post_data[key] = self.get_arguments(key)
#         self.yuyue(input, post_data)
#
#
#     def yuyue(self, parentid, post_data):
#         # 预约
#         if self.muser_vip.get_yuyue_num() > 0:
#             uid = post_data['def_uid'][0]
#             post_data = {}
#             for key in self.request.arguments:
#                 post_data[key] = self.get_arguments(key)[0]
#
#             d1 = datetime.datetime.now()
#             d3 = d1 + datetime.timedelta(hours=10)
#
#             now = int((time.time()) / (86400)) * 86400
#             secday = int(post_data['yyday']) * 24 * 3600
#             sechour = int(post_data['yyhour']) * 3600
#             setmin = int(post_data['yymin']) * 60
#             wl = now + secday + sechour + setmin
#             timeArray = time.localtime(wl)
#             otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
#             par_arr = [uid, wl, otherStyleTime]
#             if self.mrefresh.insert_data(par_arr) == True:
#                 self.muser_vip.yuyue_num_decrease(parentid)
#
#
# class DelAppointHandler(OpHandler):
#     def get(self, input=''):
#         # print(input)
#         tmp_uu = input.split(r'/')
#         if len(tmp_uu) == 3:
#             pass
#         else:
#             self.render('404.html')
#             return
#         uid, action, parentid = input.split('/')
#         if len(input) > 0:
#             if self.mrefresh.del_by_id(uid) == True:
#                 self.muser_vip.yuyue_num_increase(parentid)
#                 self.op_redirect(input)
#         else:
#             self.render('404.html')
#         # self.redirect('/tui/{0}/{1}'.format(tmp_uu[2], tmp_uu[1]))


class DeleteHandler(OpHandler):
    '''
    url:  /refresh/uid/cation/parentid
    '''

    def get(self, input=''):
        tmp_uu = input.split(r'/')
        uid = tmp_uu[0]
        self.edit_delete(uid)
        self.op_redirect(input)

    def edit_delete(self, def_uid):
        info = self.minfo.get_by_id(def_uid)
        if self.is_editable(info) == True:
            self.minfo.delete_by_uid(def_uid)

    def is_editable(self, info):
        '''
        谁发布的谁编辑
        '''
        if info['userid'] == self.user_name:
            return True
        return False


class RefreshHandler(OpHandler):
    '''
    url:  /refresh/uid/cation/parentid
    '''

    def get(self, input=''):
        url_arr = input.split(r'/')
        uid = url_arr[0]
        action = url_arr[1]
        if len(url_arr) == 3:
            parentid = url_arr[2]
            if self.muser_vip.get_refresh_num() > 0:
                if self.active_info(uid, 'refresh') == True:
                    self.update_userinfo('refresh', parentid)
                    self.set_status(200)
        else:
            if self.muser_num.get_refresh_num() > 0:
                if self.active_info(uid, 'refresh') == True:
                    self.update_userinfo('refresh')
                    self.set_status(200)

        self.op_redirect(input)


class TuiguangHandler(OpHandler):
    '''
    url:  /tuiguang/uid/cation/parentid
    '''

    def get(self, input=''):
        tmp_arr = input.split(r'/')
        if len(tmp_arr) == 3:
            pass
        else:
            return False
        uid, action, parentid = input.split(r'/')

        if self.muser_vip.get_tuiguang_num(parentid) > 0:
            if self.active_info(uid, 'tuiguang') == True:
                self.active_info(uid, 'refresh')
                self.update_userinfo('tuiguang', parentid)

        self.op_redirect(input)


class ZhidingHandler(OpHandler):
    '''
    url:  /tuiguang/uid/cation
    '''

    def get(self, input=''):
        tmp_uu = input.split(r'/')
        if len(tmp_uu) == 2:
            pass
        else:
            self.render('404.html')
            return False
        uid = tmp_uu[0]

        if self.muser_num.get_zhiding_num() > 0:
            if self.active_info(uid, 'zhiding') == True:
                self.update_userinfo('zhiding')

        self.op_redirect(input)
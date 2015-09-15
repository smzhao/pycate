# # -*- coding:utf-8 -*-
# '''
# 会员后台管理
# '''
#
# from pycate.model.shoucang_model import MShoucang
# import core.base_handler as base_handler
#
#
# class TuiHandler(base_handler.PycateBaseHandler):
#     def initialize(self, hinfo=''):
#         self.init_condition()
#         self.mshoucang = MShoucang()
#
#     def get(self, url_str=''):
#         if len(url_str) > 0:
#             par_arr = url_str.split('/')
#         if self.user_name is None or self.user_name == '':
#             self.redirect('/member/login')
#         if url_str == '':
#             self.set_status(400)
#             self.render('404.html')
#         elif len(par_arr) > 0:
#             self.listcity(par_arr)
#         else:
#             self.set_status(400)
#             self.render('404.html')
#
#
#     def get_condition(self, switch):
#         '''
#         用于listcity()，获取列出的条件。
#         '''
#         if switch == 'all':
#             condition = {'userid': self.user_name}
#         elif switch == 'notrefresh':
#             # 过期
#             condition = {'userid': self.user_name, 'def_refresh': 0, 'def_banned': 0, 'def_valid': 1}
#         elif switch == 'normal':
#             # 正常发布的
#             condition = {'userid': self.user_name, 'def_refresh': 1, 'def_banned': 0, 'def_valid': 1}
#         elif switch == 'banned':
#             # 过期
#             condition = {'userid': self.user_name, 'def_banned': 1}
#         elif switch == 'novalid':
#             # 未审核信息
#             condition = {'userid': self.user_name, 'def_banned': 0, 'def_valid': 0}
#         elif switch == 'tuiguang':
#             condition = {"catid": {"$in": self.muser_info.get_vip_cats()}, 'userid': self.user_name}
#         elif switch == 'notg':
#             condition = {"catid": {"$in": self.muser_info.get_vip_cats()},
#                          'userid': self.user_name,
#                          'def_tuiguang': 0}
#         elif switch == 'jianli':
#             condition = {'userid': self.user_name, 'parentid': '0900'}
#         elif switch == 'zhaopin':
#             condition = {'userid': self.user_name, 'parentid': '0700'}
#         return (condition)
#
#     def get_vip_menu(self, pararr):
#         parentid = pararr[0]
#         switch = pararr[1]
#         head_menu = ''
#         ac1 = ''
#         ac2 = ''
#         ac3 = ''
#         if switch == 'all':
#             ac1 = 'activemenu'
#         elif switch == 'notrefresh':
#             ac2 = 'activemenu'
#         elif switch == 'notg':
#             ac3 = 'activemenu'
#         if len(pararr) == 2:
#             head_menu = '''<ul class="vipmenu">
#             <li><a onclick="js_show_page('/tui/{0}/all')" class="{1}">所有消息</a></li>
#             <li><a onclick="js_show_page('/tui/{0}/notrefresh')" class="{2}">过期消息</a></li></ul>
#             <li><a onclick="js_show_page('/tui/{0}/notg')" class="{3}">未推广</a></li></ul>
#             '''.format(parentid, ac1, ac2, ac3)
#         return (head_menu)
#
#     def listcity(self, pararr):
#         # 所有的都是list下面的
#         parentid = pararr[0]
#         switch = pararr[1]
#         if parentid in self.muser_info.get_vip_cats():
#             pass
#         else:
#             self.write('<span class="red">联系管理员开通此分类的VIP推广权限.</span>')
#             return
#         condition = self.get_condition(switch)
#         condition['parentid'] = pararr[0]
#
#         user_published_infos = self.minfo.get_by_condition(condition)
#         kwd = {
#             'cityid': self.city_name,
#             'cityname': self.mcity.get_cityname_by_id(self.city_name),
#             'vip_cat': self.muser_info.get_vip_cats(),
#             'action': switch,
#             'parentid': parentid,
#             'head_menu': self.get_vip_menu(pararr)
#         }
#         wuserinfo = self.muser_info.get_by_username()
#         wuservip = self.muser_vip.get_by_parentid(parentid)
#         print(switch)
#         if parentid == 'zhaopin':
#             self.render('tpl_user/p_list_jianli.html',
#                         user_published_infos=user_published_infos,
#                         kwd=kwd,
#                         wuserinfo=wuserinfo,
#                         wuservip=wuservip,
#             )
#         elif parentid == '0700':
#             self.render('tui/tui_listcity.html',
#                         user_published_infos=user_published_infos,
#                         kwd=kwd,
#                         wuserinfo=wuserinfo,
#                         wuservip=wuservip,
#             )
#         elif parentid == '0300':
#             self.render('tui/tui_0300.html',
#                         user_published_infos=user_published_infos,
#                         kwd=kwd,
#                         wuserinfo=wuserinfo,
#                         wuservip=wuservip,
#             )
#         else:
#             self.render('tui/tui_listcity.html',
#                         user_published_infos=user_published_infos,
#                         kwd=kwd,
#                         wuserinfo=wuserinfo,
#                         wuservip=wuservip,
#             )
#

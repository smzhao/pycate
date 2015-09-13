# # -*- coding:utf-8 -*-
#
# import libs.tool
#
# from pycate.model.catalog_model import MCatalog
# from pycate.model.link_model import MLink
# from pycate.model.coupon_model import MCoupon
# import core.base_handler as base_handler
#
#
# class CouponHandler(base_handler.PycateBaseHandler):
#     def initialize(self, hinfo=''):
#         self.init_condition()
#
#         self.mlink = MLink()
#         self.mcat = MCatalog()
#         self.mcoupon = MCoupon()
#
#
#     def get(self, input=''):
#         # Todo: 验证
#         if input.startswith('grap'):
#             # self.render()
#             self.grap(input)
#         elif input.startswith('getinfo'):
#             self.get_info(input)
#         else:
#             op, catid = input.split(r'/')
#             if op == 'get_list':
#                 self.get_list()
#
#     def delete_by_id(self, input):
#         op, uid = input.split('/')
#         self.mlink.delete_by_uid(uid)
#         self.list()
#         # self.redirect('/link/list')
#
#     def get_info(self, input):
#         tel = input.split('/')[1]
#
#         if len(tel) < 11:
#             self.write('')
#             return
#         user_info = self.muser_info.get_by_tel(tel)
#         if user_info is None:
#             self.write('没找到用户')
#             return
#
#         coupon_id = user_info['coupon_uid']
#         coupon_info = self.mcoupon.get_by_id(coupon_id)
#         if coupon_info is None:
#             self.write('没找到该用户的优惠！')
#             return
#
#         kwd = {
#             'title': coupon_info['title'],
#             'address': coupon_info['address'],
#             'username': user_info['user_name'],
#             'company': coupon_info['company'],
#         }
#         self.render('coupon/user_info.html', kwd=kwd)
#
#     def grap(self, input):
#         self.muser_info.coupon_num_decrease(self.user_name)
#
#         coupon_uid = input.split('/')[1]
#         user_info = self.muser_info.get_by_username(self.user_name)
#         now = libs.tool.get_timestamp()
#         if now - user_info['coupon_timestamp'] < 30 * 24 * 3600:
#             self.render_yiyou()
#         elif user_info['coupon_num'] == 0:
#             self.render_out_num()
#
#         else:
#             coupon_info = {
#                 'coupon_uid': coupon_uid,
#                 'coupon_timestamp': now,
#                 'userid': self.user_name,
#                 'remainnum': user_info['coupon_num'],
#             }
#             self.muser_info.update_coupon(coupon_info)
#
#
#     def render_out_num(self):
#         self.render('coupon/out_num.html')
#
#     def render_yiyou(self):
#         user_info = self.muser_info.get_by_username(self.user_name)
#
#         coupon_id = user_info['coupon_uid']
#         coupon_info = self.mcoupon.get_by_id(coupon_id)
#         if coupon_info is None:
#             self.write('没找到该用户的优惠！')
#             return
#
#         kwd = {
#             'title': coupon_info['title'],
#             'address': coupon_info['address'],
#             'username': user_info['user_name'],
#             'company': coupon_info['company'],
#         }
#         self.render('coupon/coupy.html', kwd=kwd)
#
#     def post(self, input=''):
#         pass

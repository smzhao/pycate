# # -*- coding:utf-8 -*-
#
# import tornado.web
#
# import libs.upload
# from pycate.model.catalog_model import MCatalog
# from pycate.model.link_model import MLink
# import core.base_handler as base_handler
#
#
# class LinkHandler(base_handler.PycateBaseHandler):
#     def initialize(self, hinfo=''):
#         self.init_condition()
#         self.mlink = MLink(self.city_name)
#         self.mcat = MCatalog()
#
#
#     def get(self, input=''):
#         # Todo: 验证
#         url_arr = input.split('/')
#         if url_arr[0] == 'add_frame':
#             self.to_add_frame(url_arr[1])
#         elif url_arr[0] == 'add':
#             self.to_add(url_arr[1])
#         elif url_arr[0] == 'view':
#             self.view(url_arr[1])
#         elif input == 'list':
#             self.list()
#         elif input.startswith('delete'):
#             self.delete_by_id(input)
#         elif input.startswith('edit'):
#             self.to_edit(input)
#         else:
#             op, catid = input.split(r'/')
#             if op == 'get_list':
#                 self.get_list()
#
#     def view(self, parentid):
#         linkinfo = self.mlink.get_links_by_parentid(parentid, self.user_name)
#         if linkinfo:
#             kwd = {
#                 'userid': self.user_name,
#                 'cityid': self.city_name,
#                 'parentid': parentid,
#             }
#             self.render('link/view.html', kwd=kwd, linkinfo=linkinfo)
#
#     @tornado.web.authenticated
#     def delete_by_id(self, input):
#         op, uid = input.split('/')
#         self.mlink.delete_by_uid(uid)
#         self.list()
#
#     def post(self, input=''):
#         if input == 'add':
#             self.add()
#         elif input.startswith('edit'):
#             self.update()
#
#     @tornado.web.authenticated
#     def add(self):
#         post_data = {}
#         for key in self.request.arguments:
#             post_data[key] = self.get_arguments(key)
#         parentid = post_data['parentid'][0]
#         if self.mlink.get_links_by_parentid(parentid,  self.user_name):
#             self.set_status(400)
#         else:
#             file_dict = self.request.files['link_image'][0]
#             # 对上传的图片进行处理
#             file_up_str = libs.upload.upload_imgfile(file_dict)
#             out_arr = {'img': file_up_str}
#             out_arr['url'] = post_data['link_url'][0]
#             out_arr['catid'] = ''
#             out_arr['cityid'] = self.city_name
#             out_arr['parentid'] = parentid
#             out_arr['username'] = self.user_name
#             self.mlink.insert_rec(out_arr)
#             self.set_status(200)
#         self.redirect('/link/view/{0}'.format(parentid))
#
#     @tornado.web.authenticated
#     def update(self):
#         post_data = {}
#         for key in self.request.arguments:
#             post_data[key] = self.get_arguments(key)
#
#         if 'elink_image' in self.request.files:
#             file_dict = self.request.files['elink_image'][0]
#             file_up_str = libs.upload.upload_imgfile(file_dict)
#             out_arr = {'img': file_up_str}
#         else:
#             out_arr = {'img': post_data['old_img'][0]}
#
#         out_arr['url'] = post_data['elink_url'][0]
#         out_arr['catid'] = post_data['ecatid'][0]
#         self.mlink.update(post_data['uid'][0], out_arr)
#         self.set_status(200)
#
#
#     def list(self):
#
#         cat_str = '''<option value='' selected >请选择</option>'''
#         for cat_id in self.muser_info.get_vip_cats():
#             cat_name = self.mcat.get_by_id(cat_id).catname
#             tmp_str = '''<option value="%s" >%s</option>''' % (cat_id, cat_name)
#             cat_str += tmp_str
#
#         infos = self.mlink.get_links_by_cityid(self.user_name, self.city_name)
#         kwd = {
#             'userid': self.user_name,
#             'cityname': '',
#             'cityid': self.city_name,
#             'cat_str': cat_str,
#             'parentid': '0000',
#             'parentlist': self.mcat.get_parent_list(),
#         }
#
#         self.render('link/list.html',
#                     infos=infos,
#                     kwd=kwd,
#                     wuserinfo=self.muser_info.get_by_username(),
#                     wuservip=self.muser_vip.get_by_username(),
#         )
#
#     @tornado.web.authenticated
#     def to_add(self, parentid):
#         kwd = {
#             'userid': self.user_name,
#             'cityid': self.city_name,
#             # 'cityname': self.mcity.get_cityname_by_id(self.city_name),
#             # 'city_select_str': city_select_str,
#             'parentid': parentid,
#             # 'parentlist': self.mcat.get_parent_list(),
#         }
#         current_link = self.mlink.get_links_by_parentid(parentid,  self.user_name)
#         if current_link:
#             self.render('link/edit.html', kwd=kwd, linkinfo = current_link)
#         self.render('link/add.html', kwd=kwd)
#
#     @tornado.web.authenticated
#     def to_add_frame(self, parentid):
#         kwd = {
#             'userid': self.user_name,
#             'cityid': self.city_name,
#             # 'cityname': self.mcity.get_cityname_by_id(self.city_name),
#             'parentid': parentid,
#             # 'parentlist': self.mcat.get_parent_list(),
#
#         }
#         self.render('link/add_frame.html', kwd=kwd,
#                     wuserinfo=self.muser_info.get_by_username(),
#                     wuservip=self.muser_vip.get_by_username())
#
#     @tornado.web.authenticated
#     def to_edit(self, input):
#         # Generate the select options for cityid
#         op, uid = input.split('/')
#         # self.mlink.delete_by_uid(uid)
#         linkinfo = self.mlink.get_by_id(uid)
#         # self.list()
#         tmp_s1 = ''
#         tmp_s2 = ''
#         tmp_s3 = ''
#         link_cityid = linkinfo.cityid.strip()
#         # print(link_cityid)
#         if link_cityid == 'changchun':
#             tmp_s1 = 'selected'
#         elif link_cityid == 'tonghua':
#             tmp_s2 = 'selected'
#         elif link_cityid == 'jilin':
#             tmp_s3 = 'selected'
#
#         # city_select_str = '''
#         # <option value="changchun" {0}>c.长春</option>
#         # <option value="tonghua" {1}>t.通化</option>
#         # <option value="jilin" {2}>j.吉林</option>
#         # '''.format(tmp_s1, tmp_s2, tmp_s3)
#         #
#
#         cat_str = '''<option value='' selected >请选择</option>
#         '''
#         # print(self.vip_cat)
#         for cat_id in self.vip_cat:
#             cat_name = self.mcat.get_by_id(cat_id).catname
#             tmp_str_jcc = ''
#             if cat_id == linkinfo.catid:
#                 tmp_str_jcc = 'selected=selected'
#             tmp_str = '''<option value="{0}" {1}>{2}</option>'''.format(cat_id, tmp_str_jcc, cat_name)
#             cat_str += tmp_str
#
#         kwd = {
#             'userid': self.user_name,
#             'cityid': self.city_name,
#             'cityname': self.mcity.get_cityname_by_id(self.city_name),
#             'cat_str': cat_str,
#             'parentid': '0000',
#             'parentlist': self.mcat.get_parent_list(),
#         }
#
#         # print(kwd)
#         self.render('link/list.html', kwd=kwd, linkinfo=linkinfo)
__author__ = 'bukun@osgeo.cn'

import tornado.web

from pycate.model.catalog_model import MCatalog
from pycate.module import imgslide_module
from pycate.module import refreshinfo_module
from pycate.module import showjianli_module

ImgSlide = imgslide_module.ImgSlide
RefreshInfo = refreshinfo_module.RefreshInfo
ShowJianli = showjianli_module.ShowJianli



class UserInfo(tornado.web.UIModule):
    def render(self, uinfo, uop):
        return self.render_string('modules/user_info.html', userinfo=uinfo, userop = uop)
class VipInfo(tornado.web.UIModule):
    def render(self, uinfo, uvip):
        return self.render_string('modules/vip_info.html', userinfo=uinfo, uservip = uvip)

class ToplineModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/topline.html')


class BannerModule(tornado.web.UIModule):
    def __init__(self, parentid=''):
        self.parentid = parentid

    def render(self):
        self.mcat = MCatalog()
        parentlist = self.mcat.get_parent_list()
        kwd = {
            'parentlist': parentlist,
            'parentid': self.parentid,
        }
        return self.render_string('modules/banner.html', kwd=kwd)


class BreadCrumb(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('modules/bread_crumb.html', info=info)


class ContactInfo(tornado.web.UIModule):
    def render(self, info):
        ip = info['userip'][0]
        uu = ip.split('.')
        uu[3] = '*'
        maskip = '.'.join(uu)
        kwd = {
            'maskip': maskip,
        }
        return self.render_string('modules/contact_info.html', post_info=info, kwd=kwd)


class BreadcrumbPublish(tornado.web.UIModule):
    def render(self, sig=0):
        kwd = {
            'sig': sig,
        }
        return self.render_string('modules/breadcrumb_publish.html', kwd=kwd)


class InfoList:
    def renderit(self, info=''):
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'
        if len(info['mymps_img']) > 0:
            imgname = info['mymps_img'][0]
        if info['def_zhiding'] == 1:
            zhiding_str = '<span class="red">（已置顶）</span>'
        if info['def_tuiguang'] == 1:
            tuiguang_str = '<span class="red">（已推广）</span>'

        list_type = info['catid']

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguan': tuiguang_str,
        }

        return self.render_string('infolist/infolist_{0}.html'.format(list_type),
                                  kwd=kwd,
                                  post_info=info)
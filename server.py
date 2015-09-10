# coding:utf-8

import os
import sys

import tornado.autoreload
import tornado.ioloop
import tornado.web
from core.urls import urls
from core.modules import *
from core.config import PORT
from core.config import cookie_secret

SETTINGS1 = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': True,
    "cookie_secret": cookie_secret,
    "login_url": "/member/login",
    'ui_modules': {'Topline': ToplineModule,
                   'Banner': BannerModule,
                   'BreadCrumb': BreadCrumb,
                   'ContactInfo': ContactInfo,
                   'BreadcrumbPublish': BreadcrumbPublish,
                   'ImgSlide': ImgSlide,
                   'ShowJianli': ShowJianli,
                   'RefreshInfo': RefreshInfo,
                   'user_info': UserInfo,
                   'vip_info': VipInfo,
    },
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    APPLICATION = tornado.web.Application(handlers=urls, **SETTINGS1)
    APPLICATION.listen(PORT)
    print ('Development server is running at http://0.0.0.0:{0}/'.format(PORT))
    print ('    >>>>')
    tornado.ioloop.IOLoop.instance().start()

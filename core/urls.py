# -*- coding:utf-8 -*-

import handlers.main_handler
import handlers.publish_handler
import handlers.add_handler
import handlers.info_handler
import handlers.list_handler
import handlers.admin_handler
import handlers.user_handler
import handlers.widget_handler
import handlers.admin_operate_handler
import handlers.search_handler
import handlers.member_handler
import handlers.link_handler
import handlers.edit_handler
import handlers.coupon_handler
import handlers.changecity_handler
import handlers.filter_handler
import handlers.info_operator
import handlers.document_handler
import handlers.tui_handler

urls = [
    (r"/info/(.*)", handlers.info_handler.InfoHandler, dict(hinfo={})),
    (r"/edit/(.*)", handlers.edit_handler.EditHandler, dict(hinfo={})),
    (r"/refresh/(.*)", handlers.info_operator.RefreshHandler, dict(hinfo={})),
    (r"/delete/(.*)", handlers.info_operator.DeleteHandler, dict(hinfo={})),
    (r"/zhiding/(.*)", handlers.info_operator.ZhidingHandler, dict(hinfo={})),
    (r"/tuiguang/(.*)", handlers.info_operator.TuiguangHandler, dict(hinfo={})),
    (r"/appoint/(.*)", handlers.info_operator.AppointHandler, dict(hinfo={})),
    (r"/delappoint/(.*)", handlers.info_operator.DelAppointHandler, dict(hinfo={})),

    # 分类
    (r"/add/(.*)", handlers.add_handler.AddHandler, dict(hinfo={})),
    (r"/list/(.*)", handlers.list_handler.ListHandler, dict(hinfo={})),

    (r"/admin/(.*)", handlers.admin_handler.AdminHandler, dict(hinfo={})),
    (r"/user/(.*)", handlers.user_handler.UserHandler, dict(hinfo={})),
    (r"/filter/(.*)", handlers.filter_handler.FilterHandler, dict(hinfo={})),
    (r"/search/(.*)", handlers.search_handler.SearchHandler, dict(hinfo={})),

    (r"/operate_user/(.*)", handlers.admin_operate_handler.AdminOperateHandler, dict(hinfo={})),
    (r"/widget/(.*)", handlers.widget_handler.WidgetHandler, dict(hinfo={})),
    (r"/publish/(.*)", handlers.publish_handler.PublishHandler, dict(hinfo={})),
    (r"/changecity/(.*)", handlers.changecity_handler.ChangeCityHandler, dict(hinfo={})),

    (r"/link/(.*)", handlers.link_handler.LinkHandler, dict(hinfo={})),
    (r"/coupon/(.*)", handlers.coupon_handler.CouponHandler, dict(hinfo={})),

    (r"/member/(.*)", handlers.member_handler.MemberHandler, dict(hinfo={})),
    (r"/document/(.*)", handlers.document_handler.DocumentHandler, dict(hinfo={})),
    (r"/tui/(.*)", handlers.tui_handler.TuiHandler, dict(hinfo={})),
    (r'/(.*)', handlers.main_handler.MainHandler, dict(hinfo={})),
]

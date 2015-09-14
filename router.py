# -*- coding:utf-8 -*-

import pycate.handlers.main_handler
import pycate.handlers.publish_handler
import pycate.handlers.add_handler
import pycate.handlers.list_handler
# import pycate.handlers.admin_handler
# import pycate.handlers.user_handler
import pycate.handlers.widget_handler
# import pycate.handlers.admin_operate_handler
import pycate.handlers.search_handler
# import pycate.handlers.member_handler
import pycate.handlers.link_handler
import pycate.handlers.edit_handler
# import pycate.handlers.coupon_handler
# import pycate.handlers.changecity_handler
import pycate.handlers.filter_handler
import pycate.handlers.info_operator
import pycate.handlers.document_handler
import pycate.handlers.tui_handler
import pycate.handlers.info_handler


urls = [
    ("/info/(.*)", pycate.handlers.info_handler.InfoHandler, dict(hinfo={})),
    ("/edit/(.*)", pycate.handlers.edit_handler.EditHandler, dict(hinfo={})),
    # ("/refresh/(.*)", pycate.handlers.info_operator.RefreshHandler, dict(hinfo={})),
    ("/delete/(.*)", pycate.handlers.info_operator.DeleteHandler, dict(hinfo={})),
    # ("/zhiding/(.*)", pycate.handlers.info_operator.ZhidingHandler, dict(hinfo={})),
    # ("/tuiguang/(.*)", pycate.handlers.info_operator.TuiguangHandler, dict(hinfo={})),
    # ("/appoint/(.*)", pycate.handlers.info_operator.AppointHandler, dict(hinfo={})),
    # ("/delappoint/(.*)", pycate.handlers.info_operator.DelAppointHandler, dict(hinfo={})),

    # 分类
    ("/add/(.*)", pycate.handlers.add_handler.AddHandler, dict(hinfo={})),
    ("/list/(.*)", pycate.handlers.list_handler.ListHandler, dict(hinfo={})),

    # ("/admin/(.*)", pycate.handlers.admin_handler.AdminHandler, dict(hinfo={})),
    # ("/user/(.*)", pycate.handlers.user_handler.UserHandler, dict(hinfo={})),
    ("/filter/(.*)", pycate.handlers.filter_handler.FilterHandler, dict(hinfo={})),
    ("/search/(.*)", pycate.handlers.search_handler.SearchHandler, dict(hinfo={})),

    # ("/operate_user/(.*)", pycate.handlers.admin_operate_handler.AdminOperateHandler, dict(hinfo={})),
    ("/widget/(.*)", pycate.handlers.widget_handler.WidgetHandler, dict(hinfo={})),
    ("/publish/(.*)", pycate.handlers.publish_handler.PublishHandler, dict(hinfo={})),
    # ("/changecity/(.*)", pycate.handlers.changecity_handler.ChangeCityHandler, dict(hinfo={})),

    # ("/link/(.*)", pycate.handlers.link_handler.LinkHandler, dict(hinfo={})),
    # ("/coupon/(.*)", pycate.handlers.coupon_handler.CouponHandler, dict(hinfo={})),

    # ("/member/(.*)", pycate.handlers.member_handler.MemberHandler, dict(hinfo={})),
    # ("/document/(.*)", pycate.handlers.document_handler.DocumentHandler, dict(hinfo={})),
    # ("/tui/(.*)", pycate.handlers.tui_handler.TuiHandler, dict(hinfo={})),
    ('/', pycate.handlers.main_handler.MainHandler, dict(hinfo={})),
]

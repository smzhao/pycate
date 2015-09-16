import socket
import os

PORT = "8004"


def hostname():
    return (socket.gethostname())


cookie_str = {
    'admin_user': 'admin_user',
    'is_login': 'islogin',
    'user': 'user'
}

# 固定文字
e = {

}
# 配置的参数  Magic String
class c(object):
    free_refresh_num_a_day = 500
    vip_refresh_num_a_day = 500
    free_publish_num_a_day = 500
    vip_publish_num_a_day = 500
    vip_tuiguang_num_a_day = 500
    vip_yuyue_num_a_day = 500
    coupon_num_a_day = 500
    info_list_per_page = 20  # list中，每页列出的数目
    refresh_timeout = 60 * 60000  # 60 * 10 * 24 * 3,
    zhiding_timeout = 60 * 60000  # 60 * 20 * 24 * 1,
    tuiguang = 60 * 60000  # 60 * 30 * 24 * 2
    rmb2jinbi = 30
    jinbi2jifen = 100
    jinbi2publish = 30
    jinbi2refresh = 40
    jinbi2zhiding = 30


timeout = {
    'refresh': 60 * 60,
    'zhiding': 60 * 60,
    'tuiguang': 60 * 60,

}
# 超时的设置
# time_out = {'refresh': 60 * 60,  # 60 * 10 * 24 * 3,
# 'zhiding': 60 * 60 ,  # 60 * 20 * 24 * 1,
#             'tuiguang': 60 * 60,  # 60 * 30 * 24 * 2
# }
#


if hostname() == 'g':
    cookie_secret = "61oET0p6;h.n/k'oi[8-8=y]hpro2kshqakjw",
    mysql = {
        'dbname': 'jihy',
        'dbuser': 'root',
        'dbpass': 'g131322',
    }

    postgresql = {
        'dbname': 'jhy',
        'dbuser': 'jhyer',
        'dbpass': 'j131322',
    }
    mongo = {
        'dbname': 'jdhby',
        'dbuser': 'bk',
        'dbpass': 'b131322',
    }
    img_base_dir = '/opt/pyweb/jihy/jihy_src/static/'

else :
    cookie_secret = "61oET0p6;h.n/k'oi[8-8=y]hpro2kshqakjw",
    mysql = {
        'dbname': 'jhy',
        'dbuser': 'root',
        'dbpass': 'g131322',
    }

    mongo = {
        'dbname': 'jdhby',
        'dbuser': 'bk',
        'dbpass': 'b131322',
    }
    img_base_dir = '/opt/pyweb/jihy/jihy_src/static/'

cookie_secret = str(cookie_secret)
mark_img = os.path.join(img_base_dir, 'fixed/mark.png')

# self.db = tornpg.Connection('localhost', 'jhy', 'jhyer', 'j131322')
#
def_field = {
    'tuiguang_out_time': 'tg_out_time',
    'zhiding_out_time': 'zd_out_time',
    'refresh_out_time': 'refresh_out_time',
    'def_create_time': 'def_create_time',
    'def_update_time': 'def_update_time',
    'def_create_time_str': 'def_create_time_str',
    'def_update_time_str': 'def_update_time_str',
    'info_uid': 'def_uid'
}

copyright = {'company': '中国科学院东北地理与农业生态研究所',
             'ICP': '吉ICP备14004848号',
             'domainame': 'http:///'}

default_touxiang = 'fixed/touxiang.jpg'

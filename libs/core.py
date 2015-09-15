#  -*- coding:utf-8 -*-

'''
针对本网站的一些核心函数
'''
__author__ = 'bukun'



def get_sub_menu_str(range2list, parentname):
    '''
    '''
    out_str = '<li class="pure-menu-heading">%s</li>' % (parentname)
    for link_rec in range2list:
        tmp_str = '<li><a href="/list/%s">%s</a></li>' % (link_rec.catid, link_rec.catname)
        out_str += tmp_str
    return (out_str)


def get_out_link_str(link_recs, func):
    '''
    生成右边侧栏广告
    '''
    out_str = ''
    for link_rec in link_recs:
        img_src = func(link_rec.img)
        tmp_str = '''<div style="margin:4px 2px 4px 2px;border:1px #dddddd solid;width:98%;">
        <a href="{0}" target="_blank"><img src="{1}" width="100%" /></a></div>
        '''.format(link_rec.url, img_src)
        out_str += tmp_str
    return (out_str)

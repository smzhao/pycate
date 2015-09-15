# -*- coding:utf-8 -*-
from pycate.model.catalog_model import MCatalog
# from pycate.model.coupon_model import MCoupon
import core.base_handler as base_handler

class MainHandler(base_handler.PycateBaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        # self.minfo = MInfo(self.city_name)
        self.mcat = MCatalog()
        # self.mcity = MCity()
        self.mcoupon = MCoupon()

    def get(self, input=''):
        if input == '':
            self.main()
        else:
            self.render('404.html')

    def main(self, input=''):
        # dbdata = self.mdb.getall()
        t1 = self.mcat.get_qian2('01')
        s1 = self.format_cat(t1, 1)
        t2 = self.mcat.get_qian2('02')
        s2 = self.format_cat(t2, 2)
        t3 = self.mcat.get_qian2('03')
        s3 = self.format_cat(t3, 3)
        t4 = self.mcat.get_qian2('04')
        s4 = self.format_cat(t4, 4)
        t5 = self.mcat.get_qian2('05')
        s5 = self.format_cat(t5, 5)
        t6 = self.mcat.get_qian2('06')
        s6 = self.format_cat(t6, 6)
        t7 = self.mcat.get_qian2('07')
        s7 = self.format_cat(t7, 7)
        t8 = self.mcat.get_qian2('08')
        s8 = self.format_cat(t8, 8)
        t9 = self.mcat.get_qian2('09')
        s9 = self.format_cat(t9, 9)
        t10 = self.mcat.get_qian2('10')
        s10 = self.format_cat(t10, 10)

        kwd = {
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            's1': s1,
            's2': s2,
            's3': s3,
            's4': s4,
            's5': s5,
            's6': s6,
            's7': s7,
            's8': s8,
            's9': s9,
            's10': s10,
            'parentid': '0000',
            'parentlist': self.mcat.get_parent_list()
        }

        coupon_infos = self.mcoupon.getall()
        self.render('mainpage/index.html', kwd=kwd,
                    coupon_infos=coupon_infos)

    def format_cat(self, input, sig):
        '''
        根据分类，生成不同的区域
        '''

        headstr = '''<div class="panel panel-info"><div class="panel-heading">
            <span id="title_{sig1}"></span>
            <span><a href='/list/{catid1}'>{catname1}</a></span>
          </div>
            <ul class="list-group">
            '''

        outstr = ''

        for rec_cat in input:
            # 记录的数目
            if rec_cat.catid == rec_cat.parentid:
                # 头
                headstr = headstr.format(sig1=sig, catid1=rec_cat.catid, catname1=rec_cat.catname )
                continue
            recout = self.minfo.get_cat_recs_count(rec_cat.catid)
            if recout > 0:
                recout = str(recout)
            else:
                recout = ''
            tmpstr = '''<li class="list-group-item">
                <a href="/list/{scatid}" title="{scatname}">{scatname}</a>
                <span>{scount}</span></li>
                '''.format(scatid=rec_cat.catid, scatname=rec_cat.catname, scount=recout)

            outstr += tmpstr

        outstr += '''</ul></div>'''
        outstr = headstr + outstr
        return (outstr)

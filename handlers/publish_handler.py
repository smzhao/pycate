# -*- coding:utf-8 -*-

# import HTMLParser

# html_parser = HTMLParser.HTMLParser()
from core import config
import tornado
from model.catalog_model import MCatalog
from model.city_model import MCity
import core.base_handler as base_handler


class PublishHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):

        self.init_condition()
        self.mcat = MCatalog()
        self.mcity = MCity()

    def to_login(self):
        # tools.markit()
        self.redirect('/member/login')
        return (True)

    @tornado.web.authenticated
    def get(self, input=''):
        url_arr = input.split('/')
        if input == '':
            self.view_class1()
        elif len(input) == 4:
            self.view_class2(input)
        elif len(input) == 5:
            self.echo_class2(input)
        elif len(url_arr) == 2 and url_arr[1] == 'vip':
            self.view_class2(url_arr[0], 1)


    def post(self, input=''):
        # print ('*' * 20)
        self.get('')


    @tornado.web.authenticated
    def echo_class2(self, input=''):
        '''
        弹出的二级发布菜单
        '''
        fatherid = input[1:]
        self.write(self.format_class2(fatherid))

    @tornado.web.authenticated
    def format_class2(self, fatherid, vip=0):
        dbdata = self.mcat.get_range2_without_parent(fatherid)
        outstr = '<ul class="list-group">'
        for rec in dbdata:
            if vip == 1:
                outstr += '''
                <a href="/add/{0}/vip" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
                '''.format(rec.catid, rec.catname)
            else:
                outstr += '''
                <a href="/add/{0}" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
                '''.format(rec.catid, rec.catname)
        outstr += '</ul>'
        return (outstr)

    @tornado.web.authenticated
    def view_class1(self, fatherid=''):
        dbdata = self.mcat.get_parent_list()
        class1str = ''
        for rec in dbdata:
            class1str += '''
             <a onclick="select('/publish/2{0}');" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
            '''.format(rec.catid, rec.catname)

        kwd = {
            'class1str': class1str,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('publish/publish.html', kwd=kwd)

    @tornado.web.authenticated
    def view_class2(self, fatherid='', vip=0):
        '''
        从第二级发布
        :param fatherid:
        :return:
        '''

        fatherid = fatherid[:2] + '00'
        kwd = {
            'class1str': self.format_class2(fatherid, vip),
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('publish/publish2.html', kwd=kwd)




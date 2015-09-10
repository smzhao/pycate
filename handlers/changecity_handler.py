# -*- coding:utf-8 -*-

from core import config
import tornado
from model.catalog_model import MCatalog
from model.city_model import MCity
import core.base_handler as base_handler


class ChangeCityHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):

        self.init_condition()
        self.mcat = MCatalog()
        self.mcity = MCity()


    def get(self, input=''):
        uu = input.split('/')
        if input == '':
            self.changecity()
        elif len(uu) == 1:
            self.set_secure_cookie('cityid', uu[0])
            self.redirect('/')

    def post(self, input=''):
        self.get('')


    def changecity(self):
        all_city = self.mcity.getall()
        kwd = {
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            'parentid': '0000',
            'parentlist': self.mcat.get_parent_list(),
        }
        self.render('changecity/city.html', kwd=kwd, city_infos=all_city)



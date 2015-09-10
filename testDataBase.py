# -*- coding:utf-8 -*-
'''
测试注册用户
'''
import sys
import os

sys.path.append(os.getcwd())

from model.info_model import MInfo

import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        # from model.info_model import MInfo
        # con = pymongo.Connection('localhost')
        # self.db = con[config.mg_cfg['dbname']]
        # self.db.authenticate(config.mg_cfg['dbuser'], config.mg_cfg['dbpass'])
        cityid = 'changchun1'
        # self.tab_info = self.db['jdhby_{0}'.format(cityid)]
        self.minfo = MInfo(cityid)

class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):


    def runTest(self):
        self.id_test = 'sadf'
        post_data = {'def_uid': self.id_test, 'dsaf':'dasfvzc',
                     'dsa':'24klj'}
        self.minfo.insert_data(post_data)
        assert ( self.minfo.get_by_id(self.id_test) == post_data )
        assert ( self.minfo.get_by_id('tt') is None )
        # self.tab_info = self.db['jdhby_{0}'.format(cityid)]
    def tearDown(self):
        # self.muser.delete_by_user('value1')
        self.minfo.delete_by_uid(self.id_test)
        pass

class DefaultWidgetSizeTestCase2(SimpleWidgetTestCase):


    def runTest(self):
        self.id_test = 'sadfsadf'
        post_data = {'def_uid': self.id_test, 'dsaf':'dasfvzc',
                     'dsa':'24klj', 'views':1}
        self.minfo.insert_data(post_data)
        for i in range(100):
            self.minfo.update_view_count(self.id_test)
        views = self.minfo.get_by_id(self.id_test)['views']
        assert ( views == 101 )
        # self.tab_info = self.db['jdhby_{0}'.format(cityid)]
    def tearDown(self):
        # self.muser.delete_by_user('value1')
        self.minfo.delete_by_uid(self.id_test)
        pass





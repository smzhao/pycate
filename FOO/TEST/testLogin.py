# -*- coding:utf-8 -*-
'''
测试注册用户
'''
import sys
import os

sys.path.append(os.getcwd())

import requests
import uuid
# import libs.tool
from model.member_model import MUser

import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        # from model.info_model import MInfo
        self.payload = {'user_name': 'giser',
                        'user_pass': 'g131322',
                        }
        self.muser = MUser('giser')
        self.r = requests.post('http://192.168.4.166:8004/login', self.payload)
        # self.r2 = requests.post('http://192.168.4.166:8004/member/regist', self.payload)

    def tearDown(self):
        # self.muser.delete_user()
        pass




class DefaultWidgetSizeTestCase2(SimpleWidgetTestCase):
    def runTest(self):
        # print(type(r.status_code)
        assert self.r.status_code == 200
        # assert self.r2.status_code == 500


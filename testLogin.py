# -*- coding:utf-8 -*-
'''
测试注册用户
'''
import sys
import os

sys.path.append(os.getcwd())

import requests

# import libs.tool
from pycate.model import MUser

import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        # from model.info_model import MInfo
        self.payload = {'user_name': 'giser',
                        'user_pass': 'g131322',
                        }
        self.muser = MUser()
        self.r = requests.post('http://jiheying.com/member/login', self.payload)
        # self.r2 = requests.post('http://192.168.4.166:8004/member/regist', self.payload)

    def tearDown(self):
        self.muser.delete_by_user('value1')




class DefaultWidgetSizeTestCase2(SimpleWidgetTestCase):
    def runTest(self):
        # print(type(r.status_code)
        assert self.r.status_code == 200
        # assert self.r2.status_code == 500


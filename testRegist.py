# -*- coding:utf-8 -*-
'''
测试注册用户
'''
import sys
import os

sys.path.append(os.getcwd())

import requests

import libs.tool
from model.user_model import MUser

import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        # from model.info_model import MInfo
        self.payload = {'user_name': 'value1', 'user_pass': 'fdfsrwe',
                        'user_pass2': 'fdfsrwe',
                        'xemail': 'asdf@163.com',
                        'xtel': '131321342'}
        self.muser = MUser()
        self.r = requests.post('http://192.168.4.166:8004/member/regist', self.payload)
        self.r2 = requests.post('http://192.168.4.166:8004/member/regist', self.payload)

    def tearDown(self):
        self.muser.delete_by_user('value1')


class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):
    def runTest(self):
        dd = self.muser.get_by_username('value1')
        assert self.payload['user_name'] == dd['user_name']
        assert libs.tool.md5(self.payload['user_pass']) == dd['user_pass']
        assert self.payload['xemail'] == dd['email']
        assert self.payload['xtel'] == dd['phone']

class DefaultWidgetSizeTestCase2(SimpleWidgetTestCase):
    def runTest(self):
        # print(type(r.status_code)
        assert self.r.status_code == 200
        assert self.r2.status_code == 500


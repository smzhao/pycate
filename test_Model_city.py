# -*- coding:utf-8 -*-



# ##  JSON

# import model.city_model
import sys
import os
sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(),'' )
from pycate.model import city_model

import unittest

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.mcity = city_model.MCity()


class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):
    def runTest(self):
        self.mcity = city_model.MCity()
        citys = self.mcity.getall()
        uus = []
        for city in citys:
            uus.append(city.cityid)
        assert 'changchun' in uus
        assert 'zcv' not in uus




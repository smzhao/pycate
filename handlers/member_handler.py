from core import config

import libs.tool
# from model.member_model import MUser
from model.catalog_model import MCatalog
from wtforms.fields import StringField
from wtforms.validators import Required
from wtforms_tornado import Form
from model.city_model import MCity

import core.base_handler as base_handler


class SumForm(Form):
    user_name = StringField(validators=[Required()])
    user_pass = StringField(validators=[Required()])
    xemail = StringField(validators=[Required()])


class MemberHandler(base_handler.BaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        # self.muser_info = MUser(self.user_name)
        self.mcat = MCatalog()
        # self.mcity = MCity()


    def get(self, input):
        if input == '':
            self.render('member/user.html')
        elif input == 'regist':
            self.page_regist()
        elif input == 'todo2':
            self.page_regist2()
        elif input == 'login':
            self.page_login()
        elif input == 'logout':
            self.logout()
        else:
            self.set_status(400)

    def post(self, input=''):
        if input == 'regist':
            self.to_regist()
        elif input == 'login':
            self.login()
        elif input == 'checkpass':
            self.check_pass()
        elif input == 'changepass':
            self.changepass()
        elif input == 'charge':
            self.charge()
        elif input == 'convert':
            self.convert()
        elif input == 'buy_refresh':
            self.buy_refresh()
        elif input == 'buy_publish':
            self.buy_publish()
        elif input == 'buy_zhiding':
            self.buy_zhiding()
        else:
            self.set_status(400)

    def page_login(self):
        kwd = {'cityid': self.city_name,
               'cityname': self.mcity.get_cityname_by_id(self.city_name),
               'parentid': '0',
               'parentlist': self.mcat.get_parent_list(),
               'message': '',
        }
        self.render('member/login.html', kwd=kwd)

    def page_regist2(self):
        kwd = {'cityid': self.city_name,
               'cityname': self.mcity.get_cityname_by_id(self.city_name),
               'parentid': '0',
               'parentlist': self.mcat.get_parent_list(), }
        self.render('member/todo2.html', kwd=kwd)

    def page_regist(self):
        kwd = {'cityid': self.city_name,
               'cityname': self.mcity.get_cityname_by_id(self.city_name),
               'parentid': '0',
               'parentlist': self.mcat.get_parent_list(), }
        self.render('member/regist.html', kwd=kwd)

    def logout(self):
        '''
        '''
        self.set_secure_cookie(config.cookie_str['is_login'], 'False')
        self.set_secure_cookie(config.cookie_str['user'], '')

        self.redirect('/member/login')

    def to_regist(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        form = SumForm(post_data)
        if form.validate():
            self.muser_info.insert_data(post_data)
            self.muser_num.insert_data(post_data)
            kwd = {
                'message': '',
            }
            self.redirect('/member/login')
            # return (True)
        else:
            self.render('404.html')
            # return (False)

    def login(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        user_name = post_data['user_name'][0]
        user_pass = libs.tool.md5(post_data['user_pass'][0])
        if self.muser_info.check_user_pass(user_name, user_pass) == True:
            self.set_secure_cookie(config.cookie_str['user'], user_name)
            self.set_secure_cookie(config.cookie_str['is_login'], 'True')
            self.set_status(200)
            self.redirect(self.get_argument('next', '/'))
        else:
            self.set_status(400)
            kwd = {'cityid': self.city_name,
                   'cityname': self.mcity.get_cityname_by_id(self.city_name),
                   'parentid': '0',
                   'parentlist': self.mcat.get_parent_list(),
                   'message': '用户名或密码不对，请重新输入。',
            }
            self.render('member/login.html', kwd=kwd)


    def changepass(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)

        if True == self.muser_info.update_password(post_data['newpass'][0]):
            self.set_status(200)
            return (True)
        else:
            self.set_status(400)
            return (False)

    def charge(self):
        amount = int(self.get_argument('amount'))
        self.muser_num.charge(amount)

    def convert(self):
        amount = int(self.get_argument('amount'))

        if self.muser_num.convert(amount):
            self.set_status(200)
        else:
            self.set_status(400)

    def buy_refresh(self):
        amount = int(self.get_argument('amount'))
        if self.muser_num.buy_refresh(amount):
            self.set_status(200)
        else:
            self.set_status(400)

    def buy_publish(self):
        amount = int(self.get_argument('amount'))
        if self.muser_num.buy_publish(amount):
            self.set_status(200)
        else:
            self.set_status(400)

    def buy_zhiding(self):
        amount = int(self.get_argument('amount'))
        if self.muser_num.buy_zhiding(amount):
            self.set_status(200)
        else:
            self.set_status(400)

    def check_pass(self):
        '''
        修改密码时，根据当前用户与用户输入的密码，
        '''
        if self.user_name == '':
            self.redirect('/member/login')
            return
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        print(post_data)
        post_old_pass = libs.tool.md5(post_data['oldpass'][0])
        db_old_pass = self.muser_info.get_by_username(self.user_name).user_pass
        print(db_old_pass)
        if post_old_pass == db_old_pass:
            self.set_status(200)
            return (True)
        else:
            self.set_status(400)
            return (False)

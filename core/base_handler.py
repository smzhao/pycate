import tornado.web
from model.info_model import MInfo
from model.member_model_info import MUserInfo
from model.member_model_num import MUserNum
from model.member_model_vip import MUserVip
from model.city_model import MCity
from model.shoucang_model import MShoucang


class BaseHandler(tornado.web.RequestHandler):
    def init_condition(self):
        userid = self.get_secure_cookie('user')
        if userid is None:
            self.user_name = ''
        else:
            self.user_name = userid.decode('utf-8')

        cityid = self.get_secure_cookie('cityid')
        if cityid is None:
            self.city_name = 'changchun'
            self.set_secure_cookie('cityid', 'changchun')
        else:
            self.city_name = cityid.decode('utf-8')
        self.minfo = MInfo(self.city_name)
        self.mcity = MCity()
        self.muser_info = MUserInfo(self.user_name)
        self.muser_num = MUserNum(self.user_name)
        # if self.muser_info.is_vip() :
        self.muser_vip = MUserVip(self.user_name)


    def get_current_user(self):
        return self.get_secure_cookie("user")

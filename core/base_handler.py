import tornado.web

from pycate.model.info_model import MInfo
# from pycate.model.member_model_info import MUserInfo
# from pycate.model.member_model_num import MUserNum
# from pycate.model.member_model_vip import MUserVip
from torlite.model.muser import MUser
from pycate.model.city_model import MCity
# from torlite.core.base_handler import Ba
class PycateBaseHandler(tornado.web.RequestHandler):
    def init_condition(self):
        self.muser = MUser()

        userid = self.get_secure_cookie('user')
        if userid is None:
            self.user_name = ''
        else:
            self.user_name = userid.decode('utf-8')




        self.city_name = 'changchun'


        self.minfo = MInfo(self.city_name)
        self.mcity = MCity()
        # self.muser_info = MUserInfo(self.user_name)

        if self.get_current_user():
            self.userinfo = self.muser.get_by_id(self.get_current_user())
        else:
            self.userinfo = None



    def get_current_user(self):
        return self.get_secure_cookie("user")

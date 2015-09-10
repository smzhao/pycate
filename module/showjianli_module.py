import tornado.web

class ShowJianli(tornado.web.UIModule):
    def render(self, jianli_dic):
        # 对传入的简历进行操作。
        return self.render_string('modules/p_jianli.html', info=jianli_dic)
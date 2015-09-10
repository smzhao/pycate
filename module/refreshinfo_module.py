import tornado.web
from model.refresh_model import MRefresh


class RefreshInfo(tornado.web.UIModule):
    def render(self, info_id, action, parentid):
        self.mrefresh = MRefresh()
        yyinfos = self.mrefresh.get_by_id(info_id)
        return self.render_string('modules/refresh_info.html', yyinfos=yyinfos, action=action, parentid=parentid)
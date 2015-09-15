
import tornado.web
class ImgSlide(tornado.web.UIModule):
    def render(self,info):
        return self.render_string('modules/img_slide.html', post_info=info)
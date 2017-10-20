from tornado.web import UIModule


class UiModule(UIModule):
    def render(self, *args, **kwargs):
        return 'Im ui_modules'

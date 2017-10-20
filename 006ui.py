# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json

import utils.uimethod
import utils.uimodules

define(name='port', default=8000, help='run port', type=int)
# define(name='version', default='0.0.1', help='version 0.0.1', type=str)


class Calcuatation:
    def sum(selfs, a, b):
        return a+b


class UiHandler(tornado.web.RequestHandler):
    def fun(self):
        return 'fun test OK'

    def get(self):
        username = self.get_argument('name', 'no')
        self.render('07module.html',
                    username=username,
                    fun=self.fun,
                    cal=Calcuatation
                    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/ui', UiHandler),
        ],
        debug=True,
        template_path='templates',
        # autoescape=None,
        static_path='static',
        ui_modules=utils.uimodules,
        ui_methods=utils.uimethod,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

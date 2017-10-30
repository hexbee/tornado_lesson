# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
import time

import utils.uimethod
import utils.uimodules

from data.user_modules import User, session

define(name='port', default=8000, help='run port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # self.set_cookie(name='cookie_name', value='cookie_text')
        # self.set_cookie(name='cookie_name', value='cookie_text', expires=time.time()+60)
        # self.set_cookie(name='cookie_name', value='cookie_text', expires_days=1)
        # self.set_cookie(name='cookie_name', value='cookie_text', path='/')
        # self.set_cookie(name='cookie_name', value='cookie_text', httponly=True)
        # self.set_cookie(name='cookie_name', value='cookie_text', max_age=120)
        # self.set_secure_cookie(name='cookie_name', value='cookie_text', expires=time.time()+3600)
        self.clear_cookie(name='cookie_name')
        # self.clear_all_cookies()
        self.write('This_is_a_cookie_test_page')


class GetCookieHandler(tornado.web.RequestHandler):
    def get(self):
        co1 = self.get_cookie(name='cookie_name')
        co2 = self.get_secure_cookie(name='cookie_name')
        self.write(co1)
        self.write(u'<br>')
        self.write(co2)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/index', IndexHandler),
            (r'/getcookie', GetCookieHandler),
        ],
        debug=True,
        template_path='templates',
        # autoescape=None,
        static_path='static',
        ui_modules=utils.uimodules,
        ui_methods=utils.uimethod,
        cookie_secret='aasdasdasfgdfsdfsdfsdf',
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

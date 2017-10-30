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
        id = self.get_secure_cookie(name='ID')
        if id:
            self.write('index---欢迎%s登录' %id)
        else:
            self.write('index---未登录')
            time.sleep(3)
            self.redirect('/cookie_login')


class CookieLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('09login.html', error=None)

    def post(self):
        username = User.by_name(self.get_argument('name', ''))
        pwd = self.get_argument('password', '')
        if username and username[0].password == pwd:
            self.set_secure_cookie(name='ID', value=username[0].username, max_age=120)
            self.write('登录成功...正在跳转...')
            time.sleep(5)
            self.redirect('/index')
        else:
            self.render('09login.html', error='登录失败！')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/index', IndexHandler),
            (r'/cookie_login', CookieLoginHandler),
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

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
from tornado.web import authenticated
from pycket.session import SessionMixin

define(name='port', default=8000, help='run port', type=int)


# def auth(func):
#     def wrapper(self, *args, **kwargs):
#         id = self.get_secure_cookie(name='ID')
#         if id:
#             return func(self, *args, **kwargs)
#         else:
#             self.redirect('/cookie_login')
#     return wrapper

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None


class IndexHandler(BaseHandler):
    # @auth
    @authenticated
    def get(self):
        self.write('<h1>index---【已登录】</h1><br>\
        <a href="/logout">退出登录</a>')


class CookieLoginHandler(BaseHandler):
    def get(self):
        next_name = self.get_argument('next', '')
        self.render('10auth.html', error=None, next_name=next_name)

    def post(self):
        next_name = self.get_argument('next', '')
        username = User.by_name(self.get_argument('name', ''))
        pwd = self.get_argument('password', '')
        if username and username[0].password == pwd:
            # self.set_secure_cookie(name='ID', value=username[0].username, max_age=120)
            self.session.set('user', username[0].username)
            time.sleep(1)
            if next_name:
                self.redirect(next_name)
            else:
                self.redirect('/index')
        else:
            self.render('10auth.html', error='登录失败...请重新登录！', next_name=next_name)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/index')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/index', IndexHandler),
            (r'/cookie_login', CookieLoginHandler),
            (r'/logout', LogoutHandler),
        ],
        template_path='templates',
        # autoescape=None,
        static_path='static',
        ui_modules=utils.uimodules,
        ui_methods=utils.uimethod,
        cookie_secret='aasdasdasfgdfsdfsdfsdf',
        login_url='/cookie_login',
        pycket={
            'engine': 'redis',
            'storage': {
                'host': '106.14.212.108',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications': 11,
                'max_connections': 2**31,
            },
            'cookies': {
                'expires_days': 30,
                'max_age': 120
            },
        },
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json

import utils.uimethod
import utils.uimodules

from data.user_modules import User, session

define(name='port', default=8000, help='run port', type=int)


class AuthError(Exception):
    def __init__(self, msg):
        super(AuthError, self).__init__(msg)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = 'no'
        self.render('08sqlalchemy.html', username=username)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('08login.html', error=None)

    def post(self):
        username = User.by_name(self.get_argument('name', ''))
        pwd = self.get_argument('password', '')
        if username and username[0].password == pwd:
            self.render('08sqlalchemy.html', username=username[0].username)
        else:
            self.render('08login.html', error='登录失败！')


class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('08register.html', error=None)

    def post(self):
        if self._check_arg():
            try:
                self._create_user()
                self.render('08login.html', error=None)
            except AuthError as e:
                self.render('08register.html', error=e)
            except Exception as e:
                self.render('08register.html', error=e)
        else:
            self.render('08register.html', error='输入错误')

    def _check_arg(self):
        username = self.get_argument('name', '')
        pwd = self.get_argument('password1', '')
        if len(username) < 10 and len(pwd) < 10:
            return True
        else:
            return False

    def _create_user(self):
        if User.by_name(self.get_argument('name', '')):
            raise AuthError('用户名已经被注册！')
        if self.get_argument('password1', '') != self.get_argument('password2', ''):
            raise AuthError('两次输入的密码不一致！')
        user = User()
        user.username = self.get_argument('name', '')
        user.password = self.get_argument('password1', '')
        session.add(user)
        session.commit()


class CancellationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('08cancellation.html', error=None)

    def post(self):
        get_username = self.get_argument('name', '')
        del_username = User.by_name(get_username)
        pwd = self.get_argument('password', '')
        if del_username and del_username[0].password == pwd:
            row = session.query(User).filter_by(username=get_username)[0]
            session.delete(row)
            session.commit()
            self.write(u'---%s:销户成功---' % get_username)
        else:
            self.render('08cancellation.html', error='销户失败，请重新输入！')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/register', RegisterHandler),
            (r'/cancel', CancellationHandler),
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

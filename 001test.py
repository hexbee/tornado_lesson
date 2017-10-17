# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json

define(name='port', default=8000, help='run port', type=int)
# define(name='version', default='0.0.1', help='version 0.0.1', type=str)


class NameHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument(name='name', default='no')
        self.write('My name is %s' % name)


class UserHandler(tornado.web.RequestHandler):
    def get(self, name, age):
        # name = self.get_argument(name='name', default='no')
        self.write('----%s---%s---' % (name, age))


class UserNameHandler(tornado.web.RequestHandler):
    def get(self, age, name):
        # name = self.get_argument(name='name', default='no')
        self.write('----%s---%s---' % (name, age))


class WriteNameHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello HAHA\n')
        user = {
            'name': 'AJ',
            'age': 18,
        }
        self.write(user)
        li = [1, 2, "a", 4, "b"]
        self.write(json.dumps(li))


class HTMLHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        name = self.get_argument('name', 'no')
        pwd = self.get_argument('password', 'no')
        st = '---name=%s---password=%s---' % (name, pwd)
        self.write(st)


class ReqHandler(tornado.web.RequestHandler):
    def get(self):
        r_ip = self.request.remote_ip
        self.write('请求的IP地址：%s<br>' % r_ip)
        self.write('请求的路由：%s<br>' % self.request.path)
        self.write('请求的URL：%s<br>' % self.request.full_url())


class FlushHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('This is '+'<br>')
        self.write('Tornado'+'<br>')
        self.flush()
        import time
        time.sleep(3)
        self.write('Wa ha ha')
        self.finish()
        self.write('en------')


class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        self.write('---%d---' % status_code)

class Error2Handler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(404, 'This is 404 error test')


class HeaderHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('headers')
        self.set_header('header_a', 'aaa')
        self.set_header('header_b', 'bbb')
        self.set_header('header_c', 'ccc')
        self.add_header('header_d', 'ddd')
        self.add_header('header_d', 'eee')
        self.add_header('header_d', 'fff')
        # self.clear_header('header_d')


class TempHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login2.html')

    def post(self):
        name = self.get_argument('name', 'no')
        pwd = self.get_argument('password', 'no')
        self.render('login2_OK.html', username=name, password=pwd)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/name', NameHandler),
            (r'/user/(.+)/([0-9]+)', UserHandler),
            (r'/username/(?P<name>.+)/(?P<age>[0-9]+)', UserNameHandler),
            (r'/write', WriteNameHandler),
            (r'/index', HTMLHandler),
            (r'/login', LoginHandler),
            (r'/request', ReqHandler),
            (r'/flush', FlushHandler),
            (r'/error', ErrorHandler),
            (r'/error2', Error2Handler),
            (r'/header', HeaderHandler),
            (r'/temp', TempHandler),
        ],
        debug=True,
        template_path='templates',
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

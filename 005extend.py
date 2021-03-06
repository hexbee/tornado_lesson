# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json

define(name='port', default=8000, help='run port', type=int)
# define(name='version', default='0.0.1', help='version 0.0.1', type=str)


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('04base.html')

class ExtendHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('name', 'no')
        self.render('05extends.html', username=username)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/base', BaseHandler),
            (r'/extend', ExtendHandler),
        ],
        debug=True,
        template_path='templates',
        # autoescape=None,
        static_path='static',
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

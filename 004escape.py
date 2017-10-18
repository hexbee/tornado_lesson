# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json

define(name='port', default=8000, help='run port', type=int)
# define(name='version', default='0.0.1', help='version 0.0.1', type=str)


class TempHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('name', 'no')
        urllist = [
            ('http://www.baidu.com', '百度'),
            ('http://www.zhihu.com', '知乎'),
            ('http://www.weibo.com', '微博'),
        ]
        atga = '<a href="http://www.baidu.com" target="_blank">__百度__</a>'
        self.render('04escape.html',
                    username=username,
                    urllist=urllist,
                    atga=atga,
                    )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/temp', TempHandler),
        ],
        debug=True,
        template_path='templates',
        # autoescape=None,
        static_path='static',
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

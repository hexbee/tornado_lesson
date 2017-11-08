# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
import time
import tornado.websocket
from data.user_modules import User, session
from tornado.web import authenticated
from pycket.session import SessionMixin
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import requests

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

define(name='port', default=8010, help='run port', type=int)


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        # current_user = self.get_secure_cookie('ID')
        current_user = self.session.get('user')
        if current_user:
            return current_user
        return None


class AbcHandler(BaseHandler):
    def get(self):
        self.write('abc---OK!')


class SyncHandler(BaseHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()
        response = client.fetch('http://127.0.0.1:8000/sync?id=14')
        print(response)
        self.write(response.body)


class CallbackHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('http://127.0.0.1:8000/sync?id=14', callback=self.on_response)
        self.write('callback---OK!<br>')

    def on_response(self, response):
        print(response)
        self.write(response.body)
        self.finish()


class GenHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, 'http://127.0.0.1:8000/sync?id=7')
        print(response)
        self.write(response.body)


class FuncHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = yield self.func()
        print(response)
        self.write(response.body)

    @tornado.gen.coroutine
    def func(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, 'http://127.0.0.1:8000/sync?id=8')
        raise tornado.gen.Return(response)


class MyFuncHandler(BaseHandler):
    executor = ThreadPoolExecutor()
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = yield self.func()
        print(response)
        self.write(response.text)

    @run_on_executor
    def func(self):
        response = requests.get('http://127.0.0.1:8000/sync?id=8')
        return response


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/sync', SyncHandler),
            (r'/abc', AbcHandler),
            (r'/callback', CallbackHandler),
            (r'/gen', GenHandler),
            (r'/func', FuncHandler),
            (r'/myfunc', MyFuncHandler),
        ],
        template_path='templates',
        static_path='static',
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

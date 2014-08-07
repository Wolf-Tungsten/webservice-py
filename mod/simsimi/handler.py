# -*- coding: utf-8 -*-
from config import SIMSIMI_URL, COOKIE, AGENT, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web
import tornado.gen
import json


class SIMSIMIHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        msg = self.get_argument('msg', default='hello')
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                SIMSIMI_URL + msg,
                method='GET',
                request_timeout=TIME_OUT,
                headers={'Cookie': COOKIE, 'User-Agent': AGENT})
            response = yield tornado.gen.Task(client.fetch, request)
            x = json.loads(response.body.decode('utf8'))
            if x[u'msg'] == 'OK':
                self.write(x[u'sentence_resp'].encode('utf8'))
                self.finish()
            else:
                self.write('error')
                self.finish()
        except:
            self.write('error')
            self.finish()
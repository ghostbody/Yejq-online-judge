# encoding=utf-8_general_ci

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("logout....")
        self.clear_cookie("user")
        self.redirect("/login")
        return

    def post(self):
        self.get()
        return

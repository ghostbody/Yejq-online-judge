# encoding=utf-8_general_ci

import os.path
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import re

import torndb

from config import *

class BaseHandler(tornado.web.RequestHandler):
    user = None
    db = None
    def initial(self):
        if not self.get_secure_cookie('user'):
            self.redirect("/login")
            return False

        username = self.get_secure_cookie("user")

        try:
            db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
        except:
            self.render("error.html", message = "Database Connection Failed")
            return False

        user_info = db.get("select * from user where username='%s'" % username)

        if user_info.authority == 0:
            self.clear_cookie("user")
            self.render("error.html", message = "You have been locked in the dark room administrator!")
            return False

        if user_info.authority == -1:
            self.render("error.html", message = "Email not Confirm!")
            return False

        self.db = db
        self.user = user_info

        return True

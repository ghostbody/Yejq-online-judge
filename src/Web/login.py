# encoding=utf-8_general_ci

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import torndb

from config import *

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_secure_cookie('user'):
            self.redirect("/")
            return
        self.render("login.html", message = "Please Login")
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        
        if username == "" or password == "":
            self.render("login.html", message = "Empty Username or Password")
            return
        
        try:
            db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
        except:
            self.render("error.html", message = "Database Connection Failed")
            return

        correct_user = db.get("select password,authority from user where username='" + username + "'")
        
        if not correct_user or correct_user.password != password:
            self.render("login.html", message = "Wrong User Or Password")
            return

        if correct_user.authority == 0:
            self.render("error.html", message = "You have been locked in the dark room administrator!")
            return 

        if correct_user.authority == -1:
            self.render("error.html", message = "Email not Confirm!")
            return

        self.set_secure_cookie("user", username)

        self.redirect("/main")

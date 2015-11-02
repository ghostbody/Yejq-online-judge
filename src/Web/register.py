# encoding=utf-8_general_ci

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import mail
import torndb

import re

from config import *

from random import Random
def random_str(randomlength=20):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        secret = self.get_argument("secret", "")
        uid = self.get_argument("uid", "")
        if secret == "" or uid == "":
            self.render("register.html", message = "")
            return

        try:
            db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
        except:
            self.render("error.html", message = "Database Connection error!")
            return

        user = db.get("select * from user where uid='%s'" % uid)

        if not user:
            self.render("register.html", message = "")
            return

        if user.authority >= 0:
            self.render("error.html", message = "Already confirm!")
            return

        if user.secret == secret:
            db.execute("update user set authority=1 where uid=%s", str(uid))
            self.render("error.html", message = "Confirmed successfully!")
            os.system("mkdir " + os.path.join(system_data_path, "submit", str(uid)))
            return
        else:
            self.render("error.html", message = "Secret Wrong!")

        self.render("register.html", message = "")

    def post(self):
        username = self.get_argument("username")
        email = self.get_argument("email")
        password = self.get_argument("password")
        confirm = self.get_argument("confirm")

        if username == "" or email == "" or password == "" or confirm == "":
            self.render("error.html", message = "Incomplete input!")
        
        if len(username) < 6 or len(username) > 16:
            self.render("error.html", message = "Username length error!")
            return

        try:
            db = torndb.Connection(db_host, db_name, user = db_user, password= db_password)
        except:
            self.render("error.html", message = "Database Connection error!")
            return
        
        exist_email = db.get("select uid from user where email='%s'" % email)

        if exist_email:
            self.render("error.html", message = "Email exist!")
            return

        if not bool(re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email,flags=0)):
            self.render("error.html", message = "Wrong email format!")
            return

        exist_username = db.get("select uid from user where username='%s'" % username)

        if exist_username:
            self.render("error.html", message = "Username exit!")
            return

        if len(password) < 8 or len(password) > 16:
            self.render("error.html", message = "Password length error!")
            return

        if confirm != password:
            self.render("error.html", message = "Confirm error!")
            return

        confirmStrig = random_str()
        db.execute("insert into user (secret, username, password, email, authority) \
         values ('%s', '%s', '%s', '%s', -1)" % (confirmStrig, username, password, email))

        uid = db.get("select uid from user where username='%s'" % username)

        mail.mailConfirm("http://222.200.180.174:8080/register?uid=%s&secret=%s" % (str(uid.uid), confirmStrig), email)
        os.system("mkdir " + os.path.join(system_data_path, "submit", str(uid.uid)))
        self.render("error.html", message = "Please confirm register in your email! or wait for the admin to confirm.")

        return

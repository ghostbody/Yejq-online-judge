# encoding=utf-8_general_ci

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from login import LoginHandler
from register import RegisterHandler
from main import MainHandler
from logout import LogoutHandler
from question import QuestionsHandler
from rank import RankHandler
from profile import ProfileHandler
from getcode import getcodeHandler
from getreport import getreportHandler
from admin import AdminHandler
from admin import AdminOperationHandler
from design import DesignHandler
from discuss import DiscussHandler
from compiler import CompilerHandler
from config import *

from tornado.options import define, options

import sys
reload(sys)
sys.setdefaultencoding('utf8')

define("port", default=8080, help="run on the given port", type=int)

class ExceptionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', message="404 not found!")
        elif status_code == 500:
            self.render('error.html', message="internal server error 500!")
        else:
            self.render('error.html', message="Error " + str(status_code))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie('user'):
            self.redirect("/login")
        else:
            self.redirect("/main")

application = tornado.web.Application([
      (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/register", RegisterHandler),
        (r"/main", MainHandler),
        (r"/questions", QuestionsHandler),
        (r"/rank", RankHandler),
        (r"/my", ProfileHandler),
        (r"/discuss", DiscussHandler),
        (r"/admin", AdminHandler),
        (r"/design", DesignHandler),
        (r"/compiler", CompilerHandler),
        (r"/s-getcode",getcodeHandler),
        (r"/s-getreport",getreportHandler),
        (r"/s-admin", AdminOperationHandler),
        (r".*", ExceptionHandler)
        ], cookie_secret="61oETzKXQYEJQONLINEJUDGEFuYh7EQnp2XdTP1o/Vo=", 
                                      static_path = os.path.join(os.path.dirname(__file__), "static"),
                                      template_path = os.path.join(os.path.dirname(__file__), "template"), 
                                      debug=True)


# application = tornado.web.Application([
#     	(r"/", IndexHandler),
#         (r"/questions", QuestionsHandler),
#         (r"/judge", AdminOperationHandler),
#         (r"/design", DesignHandler),
#         ], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=", 
#                                       static_path = os.path.join(os.path.dirname(__file__), "static"),
#                                       template_path = os.path.join(os.path.dirname(__file__), "template"), 
#                                       debug=True)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = application
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

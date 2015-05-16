 
import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os.path
import re
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from lib.session import Session, SessionManager
from uimodules import Paginator

from handlers.handler import MainHandler,SubscribeHandler,LoginHandler,AdminHandler,AddHandler,DetailHandler,DeleteHandler

define("port", default = 8080, type = int)
define("mysql_host", default = "127.0.0.1")
define("mysql_database", default = "pmnews")
define("mysql_user", default = "root")
define("mysql_password", default = "")

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
            "static_path" : os.path.join(os.path.dirname(__file__), "static"),
           # xsrf_cookies = True,
            "cookie_secret" : "cookie_secret_code",
            "login_url" : "/login",
            "ui_modules" : {"Paginator":Paginator}
        }

        handlers = [
            (r"/",MainHandler),
            (r"/subscribe",SubscribeHandler),
            (r"/login",LoginHandler),
            (r"/admin",AdminHandler),
            (r"/admin/add",AddHandler),
            (r"/(.*)/delete",DeleteHandler),
            (r"/(.*)/detail",DetailHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = SessionManager(settings["cookie_secret"], ["127.0.0.1:11211"], 0)


        self.db = torndb.Connection(
            host = options.mysql_host, database = options.mysql_database,
            user = options.mysql_user, password = options.mysql_password
        )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


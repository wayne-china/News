#!/usr/bin/env python
# coding=utf-8

from tornado.web import RequestHandler
from db import news
import lib.session


class BaseHandler(RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = lib.session.Session(self.application.session_manager, self)

    @property
    def db(self):
        return self.application.db

    @property
    def news_model(self):
        return news.NewsModel(self.application.db)


    @property
    def user_model(self):
        return news.UserModel(self.application.db)

    @property
    def email_model(self):
        return news.EmailModel(self.application.db)


    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if not username: return None
        return self.user_model.get_user_by_name(username)


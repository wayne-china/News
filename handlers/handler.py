from tornado.web import RequestHandler
from base import BaseHandler
import requests
import tornado
import requests
import re


def do_login(self,user_id):
    user_info = self.user_model.get_user_by_uid(user_id)
    username = user_info["username"]
    password = user_info["password"]
    try:
        self.session["username"] = username
        self.session["password"] = password
        self.session.save()
        self.set_secure_cookie("username", str(username)) 
    except Exception,e:
        print e

def login_out(self):
    self.session["username"] = None
    self.session["password"] = None
    self.session.save()

    self.clear_cookie("username") 



class MainHandler(BaseHandler):
   
    def get(self,template_variables = {}):
    	current_page = int(self.get_argument('page',1))
    	start_point = (current_page - 1)* 5
    	page_size = 5
    	page_timeline = self.news_model.get_news_by_page(start_point,page_size)
    	whole_timeline = self.news_model.get_all_news()
    	results = len(whole_timeline)
    	template_variables["news_timeline"] = page_timeline
    	template_variables["current_page"] = current_page
    	template_variables["results"] = results
    	self.render("index.html",**template_variables)


class LoginHandler(BaseHandler):
    def get(self,template_variables = {}):
		user_info = self.get_current_user() 
		# if user_info:
		# 	self.redirect("/")
		# else:
		self.render("login.html",**template_variables)

    def post(self,template_variables = {}):
        username = self.get_argument("username")
        password = self.get_argument("password")

        secure_password = password
        #secure_password = hashlib.sha1(password).hexdigest()


        userinfo = self.user_model.login(username,secure_password)
        if userinfo:
            do_login(self,userinfo["id"])
            # template_variables["username"] = userinfo["username"]
            self.redirect("/admin",**template_variables) 
        else:
            self.write("Password wrong!")
       # self.redirect("/login")



class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,template_variables = {}):
        news_timeline = self.news_model.get_all_news()
        template_variables["news_timeline"] = news_timeline
        self.render("admin.html",**template_variables)


class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,template_variables = {}):
        self.render("add.html")

    @tornado.web.authenticated
    def post(self,template_variables = {}):
        news_name = self.get_argument("news")
        news_link = self.get_argument("link")
        try:
            self.news_model.add_news(news_name,news_link)
            return self.redirect("/admin")
        except Exception,e:
            print (e)

class DetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,news_id,template_variables = {}):
        if(re.match(r'^\d+$', news_id)):
            news = self.news_model.get_news_by_id(news_id)
        else:
            return self.write("news not found")
        template_variables["news"] = news
        self.render("detail.html",**template_variables)

class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,news_id,template_variables = {}):
        if(re.match(r'^\d+$',news_id)):
            try:
                self.news_model.del_news_by_id(news_id)
            except Exception.e:
                print(e)
            self.redirect("/admin")

        else:
            return self.write("news not found")
        

class SubscribeHandler(BaseHandler):
    pass
# 	def post(self):
# 		self.render("")


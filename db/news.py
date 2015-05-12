import torndb


class NewsModel():
    def __init__(self,db):
        self.db = db
        self.table_name = "news"

    def get_all_news(self):
        sql = "SELECT * FROM %s  ORDER BY id DESC " % (self.table_name)
        return self.db.query(sql)

    def get_news_by_page(self,begin,size):
        sql = "SELECT * FROM %s  ORDER BY id DESC LIMIT %s,%s " % (self.table_name,begin,size)
        return self.db.query(sql)

    def get_all_news_name(self):
        sql = "SELECT news_name FROM %s ORDER BY id DESC" % (self.table_name)
        return self.db.query(sql)

    def get_link_by_name(self,name):
        sql = "SELECT news_link FROM %s" % (self.table_name)
        return self.db.query(sql)



class UserModel():
    def __init__(self,db):
        self.db = db
        self.table_name = "user"

    def login(self,username,password):
        sql = "SELECT * FROM %s WHERE username = '%s' AND password = '%s' " % (self.table_name,username,password)
        return self.db.get(sql)

    def get_user_by_uid(self,uid):
        sql = "SELECT * FROM %s WHERE id=%s" % (self.table_name,uid)
        return self.db.get(sql)

    def get_user_by_name(self,username):
        sql = "SELECT * FROM %s WHERE username= '%s' " % (self.table_name,username)
        return self.db.get(sql)

class EmailModel():
    def __init__(self,db):
        self.db = db
        self.table_name = "email"

    def add_new_email(self,email):
        sql = "INSERT INTO %s ( email ) VALUES ( '%s' )" % (self.table_name,email)
 
"""
dict项目用于处理数据
"""
import pymysql
import hashlib

#编写功能类给服务端使用
class Database:
    def __init__(self,host='localhost',
                     port=3306,
                     user='root',
                     passwd='123456',
                     database='project',
                     charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db() #链接数据库

    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)
    #创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    #关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    #处理注册
    def register(self,name,passwd):
        sql = "select * from users where name = '%s'"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()#如果有结果
        if r:
            return False
        #加密处理
        hash = hashlib.md5((name+"the-salt").encode())
        hash.update(passwd.encode())
        sql = "insert into users (name,pwd) values (%s,%s)"

        try:
            self.cur.execute(sql,[name,hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    #处理登录
    def do_login(self,name,passwd):
        sql = "select * from users where name = %s and pwd = %s"
        # 　name + the-salt -->盐
        hash = hashlib.md5((name + "the-salt").encode())
        hash.update(passwd.encode())
        self.cur.execute(sql,[name,hash.hexdigest()])

        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    #处理查询
    def select(self,word):
        sql = "select mean from dict where word = '%s'"%word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    #添加历史记录
    def into_hist(self, name, word, time):
        sql = "insert into records (name,word,time) values (%s,%s,%s)"
        try:
            self.cur.execute(sql, [name, word, time])
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False

    #查看历史记录
    def do_hist(self,name):
        sql = "select name,word,time from records where name = '%s' order by  id desc limit 10"%name
        self.cur.execute(sql)
        r = self.cur.fetchall()
        if r:
           return r



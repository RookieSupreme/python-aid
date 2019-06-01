import pymysql
import re

# 链接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='123456',
                     database='project',
                     charset='utf8')

# 　获取游标
cur = db.cursor()



# 数据操作
word = open("/home/tarena/data/project/dict.txt",'r')
a = word.readlines()
sql = "insert into dict(word,mean) values(%s,%s);"
#执行ｓｑｌ语句
for i in a:
    tup =re.findall(r'(\w+)\s+(.*)',i)[0]
    try:
        cur.execute(sql,tup)
    # 　将修改内容提交到数据库
        db.commit()
    except Exception as e:
        print("有误")
        db.rollback()
        break

# 关闭游标和数据库链接
cur.close()
db.close()









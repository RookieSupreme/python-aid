"""
dict服务端
处理请求逻辑
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from time import ctime,sleep
from operation_db import *

#全局变量
HOST = '0.0.0.0'
POST = 8000
ADDR = (HOST,POST)

#处理登录
def _login(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]

    if db.do_login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fasle')

#处理注册
def do_register(c,db,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'False')

#处理查询单词
def do_select(c, db, data):
    tmp = data.split(' ')
    word = tmp[1]
    name = tmp[2]
    mean = db.select(word)
    if mean:
        c.send(mean.encode())
    else:
        c.send(b'False')
    db.into_hist(name,word,ctime())

#处理历史记录
def do_hist(c, db, data):
    tmp = data.split(' ')
    name = tmp[1]
    result = db.do_hist(name)
    if not result:
        c.send(b'Flase')
        return
    for i in result:
        msg = '%s %s %s'%i
        sleep(0.01)
        c.send(msg.encode())
    sleep(0.01)
    c.send(b'##')

#处理客户端请求
def do_request(c,db):
    db.create_cursor() # 生成游标
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit("客户端退出")
        if data[0] == 'R':
            do_register(c,db,data)
        if data[0] == 'L':
            _login(c,db,data)
        if data[0] == 'C':
             do_select(c, db, data)
        if data[0] == 'H':
             do_hist(c, db, data)

#网络链接
def main():
    #创建数据库链接对象
    db = Database()
    #创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    #等待客户端链接
    print("listen the port 8000")
    while True:
        try:
            c,addr = s.accept()
            print("connect from",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request,args=(c,db))
        p.daemon = True
        p.start()

if __name__ == "__main__":
    main()













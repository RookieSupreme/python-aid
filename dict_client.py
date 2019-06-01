"""
dict客户端
发起请求，展示结果
"""
from socket import *
from getpass import getpass

ADDR = ('127.0.0.1',8000)
s = socket()
s.connect(ADDR)

#二级界面
def login(name):
    while True:
        print("""
        ==============Query==============
        1.查单词    2.历史记录    3.注销
        =================================
        """)
        cmd = input("请输入:")
        if cmd == '1':
            do_select(name)
        elif cmd == '2':
            hist(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确命令!")

#处理登录
def do_login():
    name = input("user：")
    passwd = getpass()
    msg = 'L %s %s'%(name,passwd)
    s.send(msg.encode())
    #等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")

#注册
def do_register():
    while True:
        name = input("user：")
        passwd = getpass("输入密码:")
        passwd1 = getpass("again:")
        if (' ' in name) or (' 'in passwd):
            print("用户名或密码不能有空格")
            continue
        if passwd1 != passwd:
            print("两次密码不相同")
            continue

        msg = 'R %s %s'%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #接受反馈
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("失败")
        return

#查询单词
def do_select(name):
    while True:
        try:
            you_put = input("请输入单词:")
        except KeyboardInterrupt:
            return
        msg = 'C %s %s'%(you_put,name)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        if data == 'False':
            print("没有这个单词")
        else:
            print(data)

#处理历史记录
def hist(name):
    msg = 'H %s'%(name)
    s.send(msg.encode())
    while True:
        data = s.recv(2048).decode()
        if data == 'Flase':
            print("没有查询记录")
            return
        if data == '##':
            return
        print(data)

#创建网络链接
def main():
    while True:
        print("""
        =============welcome=============
        1.注册    2.登录    3.退出
        =================================
        """)
        cmd = input("请输入:")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            print("谢谢使用")
            return
        else:
            print("请输入正确命令!")

if __name__ == '__main__':
    main()












"""
    dict客户端
"""
from socket import *
import sys
from time import sleep

# 服务器地址
ADDR = ("127.0.0.1", 8888)


def main_l1():
    print("=======一级界面========")
    print("=======登入：login========")
    print("=======注册：register=====")
    print("=======退出：exit=====")


def main_l2():
    print("=======二级界面========")
    print("=======查字典：lookup========")
    print("=======历史记录：history=====")
    print("=======注销：logout=====")


# 客户端网络搭建
def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    while True:
        main_l1()
        cmd = input("请输入选项:")
        if cmd == "login":
            do_login(sockfd)
        elif cmd == "register":
            do_register(sockfd)
        elif cmd == "exit":
            sockfd.send(b"Q")
            sys.exit("退出字典")
        else:
            print("无此功能")


def deep_func(sockfd, name):
    while True:
        main_l2()
        func = input(">>")
        if func == "lookup":
            do_lookup(name, sockfd)
        elif func == "history":
            sockfd.send(b"H")
            sleep(1)
            data = sockfd.recv(1024).decode()
            print(data)
        elif func == "logout":
            break


def do_lookup(name, sockfd):
    while True:
        word = input("word:")
        if word:
            word = f"V {name}:{word}"
            sockfd.send(word.encode())
            data = sockfd.recv(1024).decode()
            print(data)
        else:
            break


def do_login(sockfd):
    while True:
        name = input("请输入账号：")
        code = input("请输入密码：")
        msg = f"L {name}:{code}"
        sockfd.send(msg.encode())
        data = sockfd.recv(1024).decode()
        if data == "pass":
            print("登入成功")
            deep_func(sockfd, name)

        else:
            print(data)
            return


def do_register(sockfd):
    while True:
        name = input("请输入账号：")
        code = input("请输入密码：")
        msg = f"R {name}:{code}"
        sockfd.send(msg.encode())
        data = sockfd.recv(1024).decode()
        if data == "ok":
            print("注册成功")
            return
        else:
            print("用户名已存在")
            return


if __name__ == "__main__":
    main()

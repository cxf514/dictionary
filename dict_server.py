"""
dic 服务端
"""
from socket import *
from multiprocessing import Process
import signal, sys

# 全局变量
from dict_db import Dictionary

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
# 提前连接数据库
db = Dictionary()


# 完成客户端请求
def handle(c,addr):
    db.cur()  # 每个子进程有自己的游标
    # 总分模式-》一个地方
    while True:
        data = c.recv(1024).decode()
        title = data.split(" ", 1)
        if title[0] == "R":
            name = title[1].split(":", 1)[0]
            code = title[1].split(":", 1)[1]
            do_register(c, name, code)
        elif title[0] == "L":
            name = title[1].split(":", 1)[0]
            code = title[1].split(":", 1)[1]
            do_login(c, name, code)
        elif title[0] == "V":
            name = title[1].split(":", 1)[0]
            word = title[1].split(":", 1)[1]
            do_lookup(c, name, word)
        elif data == "H":
            view_history(c)
        elif data == "Q":
            sys.exit(f"{addr}退出连接")



def view_history(c):
    for a, b, d, e in db.view_history():
        c.send(f"序号{a},单词{b},用户{d},时间{e}\n".encode())


def do_register(c, name, code):
    if db.register(name, code):
        c.send(b'ok')
    else:
        c.send(b'wrong')


def do_lookup(c, name, word):
    db.record_history(name, word)
    msg = db.lookup(word)
    c.send(msg.encode())


def do_login(c, name, code):
    if db.login(name, code) == "pass":
        c.send(b'pass')
    elif db.login(name, code) == "count error":
        c.send("此用户不存在".encode())
    elif db.login(name, code) == "code error":
        c.send("密码错误".encode())


# 搭建基本网络结构模型，启动服务
def main():
    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(10)
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # 循环等待客户端连接
    print(f"Listen the port {PORT}")
    while True:
        try:
            c, addr = sockfd.accept()
            print(f"Connect from {addr}")
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        # 为客户端创建子进程
        p = Process(target=handle, args=(c,addr))
        p.daemon = True
        p.start()


if __name__ == "__main__":
    main()

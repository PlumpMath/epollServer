#-*-coding:utf8 -*-
import socket
import select
import time
import urlApp
import webServer
from http_parse import handle_connection

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ''
port = 9999
s.bind((host,port))
s.listen(1)
print "server is running,listen ",port
s.setblocking(0)  #非阻塞
epoll = select.epoll()
epoll.register(s.fileno(),select.EPOLLIN)  #注册 文件描述符可读写
connections = {}
requsets = {}
responses = {}
while True:
    events = epoll.poll(5)  #等待激活事件,返回事件表
    if not events:
        continue
    for fileno,event in events:
        if fileno == s.fileno():
            conn ,addr = s.accept()
            conn.setblocking(0)
            epoll.register(conn.fileno(),select.EPOLLIN)
            connections[conn.fileno()] = conn
            requsets[conn.fileno()] = ""
            responses[conn.fileno()] = ""
        elif event & select.EPOLLIN:
            responses[fileno] =str(handle_connection(connections[fileno]))
                #接受完成 准备写数据
            epoll.modify(fileno,select.EPOLLOUT)

        elif event & select.EPOLLOUT:
            result = "error"
            responses[fileno] = eval(responses[fileno])
            if responses[fileno][0] == "GET":
                ob = urlApp.application.get(responses[fileno][-2])
                if ob == None:
                    result = "404"
                else:
                    result = ob.get()
            elif responses[fileno][0] == "POST":
                ob = urlApp.application.get(responses[fileno][-2])
                if ob == None:
                    result = "404"
                else:
                    result = ob.post()
  
            bytewrite = connections[fileno].send(result)
            epoll.modify(fileno, 0)
            connections[fileno].shutdown(socket.SHUT_RDWR)
        elif event & select.EPOLLHUP:
            epoll.unregister(fileno)
            connections[fileno].close()
            del connections[fileno]
epoll.unregister(connections[fileno])
s.close()



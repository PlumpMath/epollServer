#-*-coding:utf8 -*-
import socket
import sys
import urlparse

def get_header(conn):
    headers = ""
    line = conn.recv(1024)
    if line is None:
        return
    else:
        headers += line
    return headers

def parse_header(req_headers):
    request_lines = req_headers.split("\r\n")
    first_line = request_lines[0].split(' ')  #以空格来分组
    method = first_line[0]     #获取提交的方式
    req_path = first_line[1]   #请求的路径
    version = first_line[2]    #http版本号
    post_params = request_lines[-1]  #post params
    (scheme,netloc,path,params,query,fragment) = urlparse.urlparse(req_path)

    return method,version,scheme,netloc,params,query,fragment,path,post_params


def handle_connection(conn):
    req_headers = get_header(conn)
    if req_headers is None:
        return
    method,version,scheme,netloc,params,query,fragment,req_path,post_params = parse_header(req_headers)  #解析http头部,返回元祖
    return method,version,scheme,netloc,params,query,fragment,req_path,post_params




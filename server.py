#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : server.py
# @Author: JohnHuiWB
# @Date  : 2018/4/11 0011
# @Desc  :
# @Contact : huiwenbin199822@gmail.com
# @Software : PyCharm


from socket import socket


class Server(object):
    """
    web server
    """
    def __init__(self, port, text_log):
        # 创建socket server
        # 默认为family=AF_INET, type=SOCK_STREAM
        # AF_INET 对应IPv4
        # SOCK_STREAM 对应TCP
        self._ss = socket()
        # 绑定端口
        self._ss.bind(('', port))
        # 每次接受一个连接
        self._ss.listen(1)

        self._text_log = text_log

    def run(self):
        """
        main
        """
        self._text_log.AppendText('Web server ready.\n')
        # 循环接受请求
        while True:
            self._deal()

    def _deal(self):
        # 建立新连接
        conn, _ = self._ss.accept()

        try:
            # 接收一个request
            message = conn.recv(1024)
            # 解析并提取文件名，并编码为utf8
            fn = message.split()[1][1:].decode('utf8')
            # 输出简单的log
            self._text_log.AppendText('GET from '+fn+'\n')
            # 读取文件，并编码为byte_like
            data = self._read_file(fn)
            # 返回200ok
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
            # 发送所以数据
            conn.sendall(data)
        except IOError:
            # 没有读取到文件
            conn.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
            conn.send(
                b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')
        finally:
            # 最后关闭连接
            conn.close()

    @staticmethod
    def _read_file(fn):
        # 解析文件类型
        file_type = fn.split('.')[-1]
        # 处理html文件
        if file_type == 'html':
            with open(fn, 'r', encoding='utf8') as fp:
                data = fp.read().encode('utf8')
        # 处理图片文件
        elif file_type in ['png', 'jpg']:
            with open(fn, 'rb') as fp:
                data = fp.read()
        # 处理其他文件
        else:
            with open(fn, 'r', encoding='utf8') as fp:
                data = fp.read().encode('utf8')
        return data

    def _close(self):
        pass


if __name__ == '__main__':
    s = Server(3000)
    s.run()

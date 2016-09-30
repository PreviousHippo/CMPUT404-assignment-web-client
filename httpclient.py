#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def connect(self, host, port):
        # use sockets!

        # set the port as 80 if port is None

        # https://docs.python.org/2/howto/sockets.html
        # create a socket
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set the port as 80 if port is None
        if port == None:
            port = 80
        # connect to web server
        con.connect((host,port))
        return con

    # get status code
    def get_code(self, data):
        code = int(data.split()[1])
        return code

    # get header
    def get_headers(self, data):
        header = (data.split("/r/n/r/n")[0])
        return header

    # get the body
    def get_body(self, data):
        body = (data.split("\r\n\r\n")[1])
        return body


    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)


    def get_host_port(self, url):

        url_parse = urlparse(url)
        host = url_parse.hostname
        path =  url_parse.path
        port = url_parse.port

        return host, path, port


    def DisplayGetMsg(self, url):
        host, path, port = self.get_host_port(url)
        msg = "GET " + path + " HTTP/1.1\r\n"
        msg += "User-Agent: Web Client\r\n"
        msg += "Host: " + host + "\r\n"
        msg += "Accept: */*\r\n"
        msg += "Connection: Close\r\n\r\n"
        return msg


    def DisplayPostMsg(self, url, args):
        host, path, port = self.get_host_port(url)
        content = ""
        if args != None:
            content = urllib.urlencode(args)
        LenContent = len(content)

        msg = "POST " + path +" HTTP/1.1\r\n"
        msg += "Host: " + host + "\r\n"
        msg += "Content-Type: application/x-www-form-urlencoded\r\n"
        msg += "Content-Length: " +str(LenContent) + "\r\n"
        msg += "Accept: */*\r\n\r\n"
        msg += content +"\r\n"
        return msg


    def GET(self, url, args=None):
        host, path, port = self.get_host_port(url)
        con = self.connect(host,port)
        msg = self.DisplayGetMsg(url)
        # send the msg
        con.sendall(msg)

        # receive the data from server
        data = self.recvall(con)
        code = self.get_code(data)
        header = self. get_headers(data)
        body = self.get_body(data)

        print data
        con.close
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, path, port = self.get_host_port(url)
        con = self.connect(host,port)
        msg = self.DisplayPostMsg(url, args)
        # send the msg
        con.sendall(msg)

        # receive the data from server
        data = self.recvall(con)
        code = self.get_code(data)
        header = self. get_headers(data)
        body = self.get_body(data)

        print data
        con.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )

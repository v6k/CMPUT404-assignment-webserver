#  coding: utf-8 
import mimetypes
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2022 v6k
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #Converting b'request....' into string: https://www.javatpoint.com/how-to-convert-bytes-to-string-in-python
        self.data = self.request.recv(1024).strip().decode()

        method = self.data.split('\r\n')[0].split(' ')[0]
        browserPath = self.data.split('\r\n')[0].split(' ')[1]
        header=""
        file = ""
        if method != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
        else:
            try:           
                if browserPath[-1] == "/":
                    browserPath += "index.html"
                actualFilePath = open("www" + browserPath, "rb")
                file = actualFilePath.read()
                #https://stackoverflow.com/questions/4219020/how-do-i-find-mime-type-in-python/4219188#4219188
                header = "HTTP/1.1 200 OK\r\nContent-Type:"+ mimetypes.guess_type(browserPath)[0]+"\r\n\r\n"
            except FileNotFoundError:
                header = "HTTP/1.1 404 Not Found\r\n\r\n"
            except IsADirectoryError:
                header = "HTTP/1.1 301 Moved Permanently\r\n\r\n"
                self.request.sendall(bytearray(header,'utf-8'))
                self.request.sendall(bytearray("Location: "+browserPath+"/", 'utf-8'))
                return    
            except TypeError:
                header = "HTTP/1.1 404 Not Found\r\n\r\n"
                self.request.sendall(bytearray(header,'utf-8'))
                return
            
        self.request.sendall(bytearray(header,'utf-8'))
        self.request.sendall(file) if file!="" else self.request.sendall(bytearray(file,'utf-8'))
        self.request.close()



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

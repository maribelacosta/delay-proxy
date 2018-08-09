#!/usr/bin/env python
__version__ = "0.1.0"

import BaseHTTPServer, SocketServer
import time
import random
import httplib

'''
Created on Apr 28, 2011

This a Python proxy to introduce delays following a random distribution 
in every package sent from a server.

This proxy is adapted from the code provided by Fabio Domingues.
Source: http://www.oki-osk.jp/esc/python/proxy/

@author: Maribel Acosta
@author: Maria-Esther Vidal
'''


class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    server_version = "basicproxy/" + __version__

    address = None
    server = None
    alpha = None
    beta = None
    seed = None
    rbufsize = None

    # Handle the income connection.
    def handle(self):

        self.address = ProxyHandler.address
        self.server = ProxyHandler.server
        self.alpha = ProxyHandler.alpha
        self.beta = ProxyHandler.beta
        self.rbufsize = ProxyHandler.rbufsize

        # Set the random seed for delays.
        ProxyHandler.seed = ProxyHandler.seed + 1
        random.seed(ProxyHandler.seed)
        
        # Handle the connection.
        self.__base_handle()           

    # Read and write the data from the server to the client. 1000000
    def _read_write(self, response):
        
        # Read response from server.
        data = response.read()

        if self.rbufsize:
            for i in range(0, len(data), self.rbufsize):
                # Prepare delay (in ms) for response.
                delay = random.gammavariate(self.alpha, self.beta)
                delay = delay / 1000.0
                print "delay", delay
                time.sleep(delay)

                # Forward chunk to client.
                self.connection.send(data[i:self.rbufsize+i])
        else:
            # Prepare delay (in ms) for response.
            delay = random.gammavariate(self.alpha, self.beta)
            delay = delay / 1000.0
            print "delay", delay
            time.sleep(delay)
        
            # Forward response to client.
            self.connection.send(data)

    # Create the GET request to the specified address.
    def do_GET(self):

        # Get the server and path 
        server = self.server.split("http://")[1]
        path = ""
        if "/" in server:
            (server, path) = server.split("/", 1)
        
        # Prepare headers: Overwrite header from incoming connection,
        # and update referer and host (server/endpoint address).
        headers = self.headers.dict
        headers["Referer"] = self.server
        headers["Host"] = server
        
        # print "server", server, "path", path, "params", self.path[2:]
        
        # Establish connection to server.
        conn = httplib.HTTPConnection(server)
        conn.request(self.command, "/" + path + "?" + self.path[2:], None, headers)
        
        # Get response and handle it with _read_write method.
        response = conn.getresponse()
        self._read_write(response)

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer): pass


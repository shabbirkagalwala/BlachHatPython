#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:00:43 2017

@author: shabbirkagalwala
"""

import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

#create a socket object 
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#pass in the IP and port we want the server to listen on
server.bind((bind_ip,bind_port))
#now we tell the server to start listening with a backlog of max connections set to 5
server.listen(5)
print("[*] Listening on %s:%d" %(bind_ip,bind_port))

#client_handling thread
def handle_client(client_socket):
    #print what the client sends
    request = client_socket.recv(1024)
    print('[*] Received %s'%request)
    
    client_socket.send('ACK!'.encode())
    client_socket.close()
    
while True:
    client,addr = server.accept()
    print('[*] Accepted Connection from: %s:%d' %(addr[0],addr[1]))
    
    #spin our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()

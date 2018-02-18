#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:37:46 2017

@author: shabbirkagalwala
"""

#TCP Client
import socket

host="0.0.0.0"
port=9999

#create a socket object
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#connect the client
client.connect((host,port))
#since we need to send bytes-like object we encode the string to bytes
string = "Sending Packet to My Python Server"
#send some data
client.send(string.encode())
#receive some data
response = client.recv(4096)
print(response)

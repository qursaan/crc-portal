#!/usr/bin/env python3
# client
import socket
import sys

#print (sys.argv[1])
acmsport = sys.argv[2]
baudrate = sys.argv[3]

HOST = sys.argv[4]  # The target IP address
FileName = sys.argv[5]
#HOST = '172.31.149.53'  # The target IP address
PORT = 50007  # The target port as used by the server
DATA = open(FileName, 'r')

BDATA = DATA.read().encode()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
s.send(acmsport)
s.send(baudrate)
s.send(BDATA)  # Put the pattern you want to send here.
s.close()


#sketch_x0bhWBR
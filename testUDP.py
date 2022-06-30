https://shengyu7697.github.io/python-udp-socket/

Echo Sever

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys, os

HOST = '0.0.0.0'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:
    indata, addr = s.recvfrom(1024)
    print('recvfrom ' + str(addr) + ': ' + indata.decode())

    outdata = 'echo ' + indata.decode()
    s.sendto(outdata.encode(), addr)

UDP Client(send user unput)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

HOST = '0.0.0.0'	#'localhost'	socket.gethostname()
PORT = 7000
server_addr = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    outdata = input('please input message: ')
    print('sendto ' + str(server_addr) + ': ' + outdata)
    s.sendto(outdata.encode(), server_addr)
    
    indata, addr = s.recvfrom(1024)
    print('recvfrom ' + str(addr) + ': ' + indata.decode())

UDP Client(every second)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time

HOST = '0.0.0.0'
PORT = 7000
server_addr = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	outdata = 'heartbeat'
	print('sendto ' + str(server_addr) + ': ' + outdata)
	s.sendto(outdata.encode(), server_addr)
	
	indata, addr = s.recvfrom(1024)
	print('recvfrom ' + str(addr) + ': ' + indata.decode())
	
	time.sleep(1)

	

https://pymotw.com/2/socket/udp.html

Echo Server

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)
    
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data
    
    if data:
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)

Echo Client

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = 'This is the message.  It will be repeated.'

try:

    # Send data
    print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
	
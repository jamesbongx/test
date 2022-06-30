import socket
import sys, os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(10)
server_address = ('localhost', 5500)
try:
	print('111111')
	sock.bind(server_address)
	print('222222')
	data, addr = sock.recvfrom(1024)
	print('recvfrom ' + str(addr) + ': ' + data.decode())
	if data:
		print('3333333')
		sent = sock.sendto(data, addr)
except socket.timeout:
	print('socket.timeout')
except socket.gaierror: 
	print('errors during search for IP addr information, ie getaddrinfo() and getnameinfo()')
except socket.error as error:
	print(os.strerror(error.errno))
	print(error)
finally:
	sock.close()
	
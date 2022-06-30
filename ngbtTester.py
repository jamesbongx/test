#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import socket
import sys, os

import json
import shutil
import codecs
import numpy as np
import copy
import xml.etree.ElementTree as ET
from lxml import etree
import enum
from datetime import datetime
import functools
import time
#from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
import tkinter.font as tkFont
#########################################################################
padLeft			= 5
padTop			= 5
spaceH			= 150
spaceV			= 50
result_width	= 600

window_Left		= 200
window_top		= 50
window_width	= 800
window_height	= 600

LOG_FILE	= r'C:\betslip\x\ngbtTst.log'
TST_SEQ_FILE= r'C:\betslip\x\testCase1.json'
TST_SEQ_PATH= 'C:\\betslip\\x\\test\\'

BETSLIP_FILE= r'C:\betslip\x\slip.bin'
REPLY_FILE	= r'C:\betslip\x\reply.bin'
XML_PATH	= 'C:\\ngbt\\XML\\'

ERRMSG_H	= 'C:\\ngbt\\COMMON\\inc\\errmsg.h'

#msg = b'Alice' = b'\x33\x34'
TX_CONNECT		= b'\x30'
TX_INSERT_SLIP	= b'\x31'
TX_NX_REPLY		= b'\x32'
TX_NX_XML		= b'\x33'
RX_CONNECT		= 0x30
RX_ERR_CODE		= 0x31
RX_NX_REPLY		= 0x32
RX_NX_XML		= 0x33

def quitAll():
	'''
	for t in threads:
		t.join()
	'''
	closeSock()
	top.destroy()
	fpLog.close()
	exit(0)
#########################################################################
def prnC(hexData):
	ret = '\\x'.join(hex(x) for x in hexData)
#	print(ret)
	cData = ''
	while len(ret) > 32:
		cData += '"{}"\n'.format(ret[0:32])
		ret = ret[32:]
	cData += '"{}"\n'.format(ret)
	print(cData)
def trimReply(hexData):
	for i in range(len(hexData) -  7):
		tmp = ''.join(chr(x) for x in hexData[i:i+2])
		if not tmp.isdigit():
			continue
		tmp = ''.join(chr(x) for x in hexData[i+2:i+5])
		if not tmp.isalpha():
			continue
		tmp = ''.join(chr(x) for x in hexData[i+5:i+7])
		if not tmp.isdigit():
			continue
		break
	return hexData[i:]
def loadReply(fname):
	fp = open(fname,'r')
	hexData = []
	try:
		for line in fp.readlines():
			items = line.split(' ')
			for item in items[1:9]:
				tmp = int(item, 16)
				hexData.append(tmp)
	except ValueError:
		hexData = trimReply(hexData)
#		ret = ''.join(chr(x) for x in hexData)
		ret = bytes(hexData)
		print(fname + ' :: ')
		print(ret)
	fp.close()
	return ret
#########################################################################
def setReply():
	global ptrReply, replys
	if ptrReply >= len(replys):
		print('no more reply')
		quitAll()
	ret = loadReply(TST_SEQ_PATH + replys[ptrReply])
	with open(REPLY_FILE, "wb") as fp:
		fp.write(ret)
	ptrReply += 1
def setXML():
	global ptrXML, xmls
	if ptrXML >= len(xmls):
		print('no more XML')
		quitAll()
	print('XML = [')
	for xmlFile in xmls[ptrXML]:
		print('\t', xmlFile)
		shutil.copy2(TST_SEQ_PATH + xmlFile, XML_PATH + xmlFile)
	print(']')
	ptrXML += 1
def setSlip():
	global ptrSlip, betSlips
	if ptrSlip >= len(betSlips):
		print('no more slip')
		quitAll()
	slipFile = betSlips[ptrSlip]
	print('slip = ', slipFile)
	shutil.copy2(TST_SEQ_PATH + slipFile, BETSLIP_FILE)
	ptrSlip += 1
def chkRemain(lst, ptr, msg):
	x = len(lst) - ptr
	ret = (x == 0)
	if not ret:
		print(x, msg)
	return ret
def chkErrCode(errCode):
	global ptrErrCode, errCodes
	expected = errCodes[ptrErrCode]
	if expected != errCode:
		print('wrong error code : rx =', errCode, '; expected =', expected)
		quitAll()
	ptrErrCode += 1
	if ptrErrCode >= len(errCodes):
		ret = chkRemain(betSlips, ptrSlip, ' slip remain')
		ret = ret and chkRemain(replys, ptrReply, ' reply remain')
		ret = ret and chkRemain(xmls, ptrXML, ' XML remain')
		print('test completed, result =', ret)
		quitAll()
	else:
		print('test result =', errCode)
#########################################################################
def initNGBT():
	global ptrErrCode, ptrReply, ptrSlip, ptrXML
	print('initNGBT')
	ptrErrCode	= 0
	ptrReply= 0
	ptrSlip	= 0
	ptrXML	= 0
	setSlip()
	setReply()
	setXML()
def errName2Code(errNames):
	global errCodes
	with codecs.open(ERRMSG_H, 'r', encoding='big5') as f:
		lines = f.readlines()
	for i, line in enumerate(lines):
		if 'enum ERROR_ID {' in line:
			break
	else:
		print('no errStart found')
		exit(0)
	lines = lines[i+1:]
	for i, line in enumerate(lines):
		if '// RID_COUNT =' in line:
			break
	else:
		print('no errEnd found')
		exit()
	lines = lines[:i]
	errorLst = []
	for line in lines:
		tmp = line.split()
		tmp = tmp[0].replace(',','')
		errorLst.append(tmp)
	errCodes = []
	for i, errName in enumerate(errNames):
		inx = errorLst.index(errName)
		errCodes.append(inx)
fpLog	= open(LOG_FILE,'w')
with codecs.open(TST_SEQ_FILE, 'r', encoding='utf-8') as f:
	TEST_FILES = json.load(f)
replys	= TEST_FILES['reply']
betSlips= TEST_FILES['betslip']
xmls	= TEST_FILES['xml']
errNames= TEST_FILES['errorName']
errName2Code(errNames)
#########################################################################
def sendByte(b):
	global sock, server_address, receiving
	if not receiving:	#sockThread.is_alive():
		print('no connection')
		return -1
	return sock.sendto(b, server_address)
def sendString(str):
	b = str.encode(encoding = 'UTF-8')
	return sendByte(b)
receiving = False
def closeSock():
	global sock, receiving
	receiving = False
	sock.close()	
def rxLoop(name):
	global sock, server_address, receiving
	print('start socket')
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#	sock.settimeout(20)
	server_address = ('localhost', 5500)
	try:
		sent = sock.sendto(TX_CONNECT, server_address)
		receiving = True
		while(receiving):
			data, addr = sock.recvfrom(1024)
#			print('recvfrom ' + str(addr) + ': ' + data.hex())	
#			str = data.decode()
#			print(str.replace('\0',''))
			cmd = int(data[0])
			print('rx command =', cmd, )
			if cmd == RX_CONNECT:
				initNGBT()
				print('insert slip')
				sendByte(TX_INSERT_SLIP)			
			elif cmd == RX_ERR_CODE:
				if len(data) >= 2:
					errCode = data[1]
					chkErrCode(errCode)
			elif cmd == RX_NX_SLIP:
				setSlip()
			elif cmd == RX_NX_REPLY:
				setReply()
			elif cmd == RX_NX_XML:
				setXML()
	except socket.timeout:
		print('socket.timeout')
	except socket.gaierror: 
		print('errors during search for IP addr information, ie getaddrinfo() and getnameinfo()')
	except socket.error as error:
		print(os.strerror(error.errno))
		print('????????????', error)
	sock.close()
	receiving = False
	print('socket closed')
'''
def hello():
    print("hello, world")
t = Timer(30.0, hello)
t.start()
'''
def startSocket():
	initNGBT()
	if not receiving:	#sockThread.is_alive():
		sockThread = threading.Thread(target=rxLoop, args=(1,), daemon=True)
		sockThread.start()
		time.sleep(0.1)
def startTest():
	startSocket()
	sendByte(TX_INSERT_SLIP)
startSocket()
###################################################################################
top = tk.Tk()
top.title('Search XML')
top.config(bg='#345')
#top.geometry("600x800+200+50")	
top.geometry(f'{window_width}x{window_height}+{window_Left}+{window_top}')
style = ttk.Style()		#(top)
#style = ttk.Style(top)
style.configure('.', font=('Helvetica', 10))

butSrh		= ttk.Button(top, text = "Quit",command = quitAll)
butSrh.place	(x = padLeft, y = padTop, width = 70, height = 30)
butInsert	= ttk.Button(top, text = "start test",command = startTest)
butInsert.place	(x = padLeft + 100, y = padTop, width = 70, height = 30)
	
top.mainloop()

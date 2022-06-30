#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import shutil
import codecs
import numpy as np
import copy
import cv2

OUT_PATH = 'out'
OUT_PATH_OK = 'outOK'

Y_BEG_BOTTOM = 400

def saveSlipNames():
	fp = codecs.open('slip.lst', "w", encoding="utf-8")
	fp.write('      ID  = Name\n')
	for i in range(len(slipIDs)):
		fp.write('{:0>3d} = {}\n'.format(slipIDs[i], slipNames[i]))
	fp.close()
def showSlipNames():
	print('      ID  = Name')
	for i in range(len(slipIDs)):
		print('{:>3d} : {:0>3d} = {}'.format(i, slipIDs[i], slipNames[i]))
def quitAll():
	cv2.destroyAllWindows()
	exit(0)
def abort(prompt):
	print(prompt)
	quitAll()
def userAbort():
	abort('User Abort')
def notExistAbort(prompt):
	showSlipNames()
	abort(prompt + ' not found, please select one of the above : ')

def inverseMask(mask):
	m = []
	for row in mask:
		lst = []
		for e in row:
			lst.append(e ^ 1)
		m.append(lst)
	return m
def genEmptyMatrix(slipCol,slipRow):
	return [[0 for x in range(slipCol)] for y in range(slipRow)]
def genEmptyMask():
	return genEmptyMatrix(slipCol,slipRow)
def resetData():
	global selected
	selected = genEmptyMask()

def getIndex(x,end,space,cnt):
	if x < end:
		for i in range(cnt + 1):
			pos = end - int(space * (i + 1))
			if x > pos:
				return cnt - i - 1
	return -1
def getIndexXsel(x):
	return getIndex(x,rightSel,spaceWsel,slipCol)
def getIndexYsel(y):
	return getIndex(y,bottomSel,spaceHsel,slipRow)
def getCooridate(x,y):
	if SHOW_BOTTOM:
		y += Y_BEG_BOTTOM
	c = getIndexXsel(x)
	r = getIndexYsel(y)
	return r,c

#			0123456789ABCDEF
chConner = '   ─ ┘└┴ ┐┌┬│┤├┼'
def getRight(i):
	return rightSel + int(spaceWsel * i)
def getRightDiff(i):
	return abs(getRight(i) - rightLine)
def showGrid(img):
	color = (255,0,0)
	thickness = 1

	i = 0
	while getRightDiff(i) > getRightDiff(i + 1):
		i += 1
	right = getRight(i)
	left = int(right - (slipCol * spaceWsel) + 0.5)
	if left < 0:
		abort('left < 0')

	for i in range(slipCol + 1):
		x = right - int(spaceWsel * i)
		cv2.line(img, (x,topSel), (x,bottomSel), color, thickness)
	for i in range(slipRow + 1):
		y = bottomSel - int(spaceHsel * i)
		cv2.line(img, (left,y), (right,y), color, thickness)

	for c in range(len(tableLine[0])):
		x = left + int(spaceWsel * c)
		Xbeg = x - int(spaceWsel / 2)
		Xend = x + int(spaceWsel / 2)
		for r in range(len(tableLine)):
			y = topSel + int(spaceHsel * r)
			Ybeg = y - int(spaceHsel / 2)
			Yend = y + int(spaceHsel / 2)
			ch = tableLine[r][c]
			if (ch & 1) != 0:
				cv2.line(img, (Xbeg,y), (x,y), color, 3)
			if (ch & 2) != 0:
				cv2.line(img, (x,y), (Xend,y), color, 3)
			if (ch & 4) != 0:
				cv2.line(img, (x,Ybeg), (x,y), color, 3)
			if (ch & 8) != 0:
				cv2.line(img, (x,y), (x,Yend), color, 3)
def getCooridateMasked(x,y):
	global maskUsed
	r,c = getCooridate(x,y)
	if maskUsed[r][c] == 0:
		return -1,-1
	return r,c
clicked = True
def findSel(x,y):
	global clicked, selected
	r,c = getCooridateMasked(x,y)
	if c >= 0 and r >= 0:
		d = selected[r][c]
		d ^= 1
		selected[r][c] = d
		clicked = True

def drawMark(img, x,y, filled):
	if filled == 0:
		thickness = 2
	else:
		thickness = -1
	cv2.circle(img,(x,y), 8,(255,0,0),thickness)
def drawMarkSel(img, row, col):
	x = int(leftSel + (col * spaceWsel) + spaceWsel / 2)
	y = int(topSel + (row * spaceHsel) + spaceHsel / 2)
	drawMark(img, x, y, True)
def drawMask(img, row, col):
	x = int(leftSel + (col * spaceWsel) + spaceWsel / 2)
	y = int(topSel + (row * spaceHsel) + spaceHsel / 2)
	drawMark(img, x, y, False)

def showSelected(img, selected):
	global SHOW_MASK
	r = 0
	for row in selected:
		c = 0
		for e in row:
			if e != 0:
				drawMarkSel(img,r,c)
			'''
			else:
				if maskUsed[r][c] != 0 and SHOW_MASK:
					drawMask(img,r,c)
			'''
			c += 1
		r += 1
def showChanges():
	global orgImg
	orgImg = cv2.imdecode (np.fromfile (imgName, dtype = np.uint8), -1)	#orgImg = cv2.imread(imgName)
	showSelected(orgImg,selected)
	showGrid(orgImg)

	img = orgImg
	if SHOW_BOTTOM:
		img = orgImg[Y_BEG_BOTTOM:,:]
	cv2.imshow('image',img)
	cv2.moveWindow('image', 200, 0)

#######################################################################
def table2data(table):
	t = np.transpose(table)	#
	mt = t.tolist()
	s = ""
	for row in mt:
		for e in row:
			s += str(e)
	return s
def writeIntX(f, i, sz):
	b = i.to_bytes(sz, byteorder="little")
	f.write(b)
def writeInt(f, i):
	print('int = ', i)
	writeIntX(f, i, 4)
def writeByte(f, i):
	print('byte = ', int(i))
	writeIntX(f, i, 1)
def writeString(f, s):
	print('str = ', s)
	b = s.encode()
	f.write(b)
def writeSlipID(f):
	st = "{:0>8b}".format(slipID)
	rStr = st[::-1]
	writeString(f, rStr)
	print('slipID = ',slipID, rStr)
def genSlipData(selected, fname):
	slipData = table2data(selected)

	f = open(fname+'.bin','wb')
	writeInt(f, slipCol)
	writeInt(f, slipRow)
	writeInt(f, 8)
	writeSlipID(f)
	sz = len(slipData)
	if sz != slipRow * slipCol:
		abort('incorrect slipData')
	writeInt(f, sz)
	writeString(f, slipData)
	writeInt(f, 0)
	name="Slip{}Colx{}Row".format(slipCol,slipRow)
	sz = len(name)
	writeInt(f, sz)
	writeString(f, name)
	writeInt(f, 1)
	writeByte(f, 0)
	writeInt(f, 1)
	writeByte(f, 0)
	f.close()

	cv2.imwrite('tmp.bmp', orgImg)
	shutil.copy2('tmp.bmp', fname + '.bmp')

#################################################################################
def setImage():
	global goodPath, confPath, cName, confName, imgName, inxImgName
	confPath = OUT_PATH + '\\' + slipName
	goodPath = OUT_PATH_OK + '\\' + slipName
	print(confPath)
	cName		=  os.path.join(confPath, r'c.txt')
	confName	= os.path.join(confPath, r'SETTINGS.json')
	imgName		=  os.path.join(confPath, r'betSlip.bmp')
	inxImgName	=  os.path.join(confPath, r'inx.bmp')

def getSettings():
	global SETTINGS
	global slipID, slipCol, slipRow
	global rightSel, bottomSel, leftSel, topSel
	global spaceWsel, spaceHsel
	global maskUsed
	global tableLine, rightLine
	setImage()

	with codecs.open(confName, 'r', encoding='utf-8') as f:
		SETTINGS = json.load(f)
	tableLine=SETTINGS['line']
	maskUsed= SETTINGS['mask']
	slipID	= SETTINGS['slipID']
	slipCol = SETTINGS['slipCol']
	slipRow = SETTINGS['slipRow']
	spaceWsel	= SETTINGS['spaceWsel']
	spaceHsel	= SETTINGS['spaceHsel']
	rightSel	= SETTINGS['rightSel']
	bottomSel	= SETTINGS['bottomSel']
	leftSel		= rightSel - int(spaceWsel * slipCol)
	topSel		= bottomSel- int(spaceHsel * slipRow)
	rightLine	= SETTINGS['rightLine']

def matrix2json(m):
	txt = '[\n'
	for j in range(len(m)):
		txt += '\t\t[\t'
		for i in range(len(m[0])):
			txt += "{:>2d}".format(m[j][i])
			txt += ','
		txt = txt[:-1] + '\t],\n'
	return txt[:-2] + '\t]'
def name2json(name):
	return '\t"{}": '.format(name)
def genJsonMatrix(name, m):
	return name2json(name) + matrix2json(m) + ',\n'
def genJsonStr(name, s):
	return name2json(name) + "'{}',\n"	.format(s)
def genJsonRaw(name, i):
	return name2json(name) + "{},\n"	.format(i)
def saveJson(data, fname):
	txt = '{\n'
	for k, v in data.items():
		if isinstance(v, list):
			txt+= genJsonMatrix(k, v)
		elif isinstance(v, str):
			txt+= genJsonStr(k, v)
		elif isinstance(v, int):
			txt+= genJsonRaw(k, v)
		elif isinstance(v, float):
			txt+= genJsonRaw(k, v)
		else:
			print(type(v))
	txt = txt[:-2] + '\n}'
	print(txt)
	print(fname)
	fp = codecs.open(fname, "w", encoding="utf-8")
	
	fp.write(txt)
	fp.close()
#################################################################################
def cutUnusedLines(tableLine):
	npMask = np.asarray(maskUsed)
	row = np.any(npMask != 0, axis = 1)
	col = np.any(npMask != 0, axis = 0)
	begR = np.argmax(row == True)
	begC = np.argmax(col == True)
	npTable = np.asarray(tableLine)

	for i in reversed(range(begR)):
		npTable = np.delete(npTable, i, axis=0)
	for i in reversed(range(begC)):
		npTable = np.delete(npTable, i, axis=1)

	npTable[:,0] |= 12
	npTable[0] |= 3
	npTable[:,-1] |= 12
	npTable[-1] |= 3
	npTable[0][0] = 10
	npTable[0][-1] = 9
	npTable[-1][0] = 6
	npTable[-1][-1] = 5

	Rs, Cs = np.where(npTable == 11)
	for i in range(len(Rs)):
		r = Rs[i]
		c = Cs[i]
		if r < slipCol:
			if (npTable[r + 1][c] & 4) == 0:
				npTable[r][c] = 3
	Rs, Cs = np.where(npTable == 7)
	for i in range(len(Rs)):
		r = Rs[i]
		c = Cs[i]
		if r > 0:
			if (npTable[r - 1][c] & 8) == 0:
				npTable[r][c] = 3
	Rs, Cs = np.where(npTable == 14)
	for i in range(len(Rs)):
		r = Rs[i]
		c = Cs[i]
		if c < slipRow:
			if (npTable[r][c + 1] & 1) == 0:
				npTable[r][c] = 12
	Rs, Cs = np.where(npTable == 13)
	for i in range(len(Rs)):
		r = Rs[i]
		c = Cs[i]
		if c > 0:
			if (npTable[r][c - 1] & 2) == 0:
				npTable[r][c] = 12

	return npTable, begR, begC
#################################################################################
MAX_TKT_COLUMN	= 36
MAX_TKT_ROW		= 22
#			0123456789ABCDEF
chMidV	 = '     │││    ││││'
chConner = '   ─ ┘└┴ ┐┌┬│┤├┼'
chMidH	 = '   ─ ─ ─ ─ ─ ─ ─'
chTop	 = '─  ─ ─ ─ ┬┬┬    '

def prnBoxChar():
	for i in range(len(chConner)):
		print('{:>2d}..{}'.format(i, chConner[i]))
def genTitle():
	title1 = '* ┌────┬'
	title2 = '* │    │'
	title3 = '* ├────┼'
	for c in range(slipCol):
		title1 += '─────'
		title2 += '{:.>4d} '.format(c + 1)
		title3 += '────' + chTop[tableLine[0][c + 1]]
	title1 = title1[:-1] + '┐'
	title2 = title2[:-1] + '│'
	title3 = title3[:-1] + '┤'
	return title1 + '\n' + title2 + '\n' + title3 + '\n'

def genLine(r, table, mask):
	body1 = '* │    │'
	body2 = '* │{:.>4d}│'.format(slipRow - r + 1)
	if r == slipRow - 1:
		body3 = '* └────┴'
	else:
		body3 = '* │    ' + chConner[tableLine[r + 1][0]]
	for c, v in enumerate(table[r]):
		body1 += '    ' + chMidV[tableLine[r + 1][c + 1]]
		if mask[r][c] != 0:
			body2 += ',{:>3d}'.format(v)
		else:
			body2 += '    '
		body2 += chMidV[tableLine[r + 1][c + 1]]
		if chMidH[tableLine[r + 1][c + 1]] == '─':
			body3 += '────'
		else:
			body3 += '    '
		body3 += chConner[tableLine[r + 1][c + 1]]
	return body1 + '\n' + body2 + '\n' + body3 + '\n'
def buildBoxedComment(table, mask):
	res = genTitle()
	for r in range(slipRow):
		res += genLine(r, table, mask)
	return res
def drawInxSel(img, row, col, v):
	x = int(leftSel + (col * spaceWsel) + 5)
	y = int(topSel + ((row + 0.5) * spaceHsel))
	str = '{:>3d}'.format(v)
	cv2.putText(img, str, (x * 2, y * 2), cv2.FONT_HERSHEY_SIMPLEX,
     1,			#font size
    (255,0,0),	#font color
     3)			#font stroke
def saveInxImg(table, mask):
	img = cv2.imdecode (np.fromfile (imgName, dtype = np.uint8), -1)
	showGrid(img)
	width = int(img.shape[1] * 2)
	height = int(img.shape[0] * 2)
	dsize = (width, height)
	output = cv2.resize(img, dsize)

	r = 0
	for row in mask:
		c = 0
		for e in row:
			if e != 0:
				drawInxSel(output, r, c, table[r][c])
			c += 1
		r += 1
		
	cv2.imwrite('tmp.bmp', output)
	shutil.copy2('tmp.bmp', inxImgName)
def buildMaskTable(table, mask):
	ret = ''
	j = 0
	for row in table:
		i = 0
		for e in row:
			if mask[j][i] != 0:
				s = "{:>3d},".format(e)
				ret += s
			else:
				ret += "    "
			i += 1
		ret += '\n'
		j += 1
	return ret
def table2String(table):
	ret = ''
	for row in table:
		for e in row:
			s = ",{:>3d}".format(e)
			ret += s
		ret += '\n'
	return ret
def genCtxt(txt):
	return '\n' + txt
def buildInxTable():
	table = []
	for y in range(MAX_TKT_ROW-slipRow+1, MAX_TKT_ROW+1):
		r = []
		for x in range(slipCol):
			i = y + x * MAX_TKT_ROW
			r.append(i)
		table.append(r)
	return table
def saveCfile():
	CFILE = {}
	inxTable = buildInxTable()
	CFILE['inxAll'] = genCtxt(table2String(inxTable))
	CFILE['inxUsed'] = genCtxt(buildMaskTable(inxTable, maskUsed))
	maskInv = inverseMask(maskUsed)
	CFILE['inxUnused'] = genCtxt(buildMaskTable(inxTable, maskInv))
	CFILE['comment'] = genCtxt(buildBoxedComment(inxTable, maskUsed))
	saveJson(CFILE, cName)
	saveInxImg(inxTable, maskUsed)
#######################################################################
def mask2select():
	global selected
	selected = copy.deepcopy(maskUsed)

def setSlip():
	global slipInx, slipName, maskUsed
	slipName = slipNames[slipInx][0]
	print(slipInx, slipName)
	getSettings()
	mask2select()
	maskUsed = genEmptyMask()
	maskUsed = inverseMask(maskUsed)
	prnBoxChar()
def setNxSlip():
	global slipInx
	slipInx += 1
	if slipInx >= len(slipIDs):
#		slipInx = 0
		abort('no more slip')
	setSlip()
def setPrevSlip():
	global slipInx, slipName
	slipInx -= 1
	if slipInx < 0:
		slipInx = len(slipIDs) - 1
	setSlip()

def processKey(keyI):
	global maskUsed, selected
	global slipID
	global SHOW_MASK, SHOW_BOTTOM

	key = chr(keyI)
	print(key)
	if key == '4':
		print('show lower part of slip')
		SHOW_BOTTOM = True
		showChanges()
		return
	elif key == '5':
		print('show upper part of slip')
		SHOW_BOTTOM = False
		showChanges()
		return
	else:
		if MODE == 'BROWSE':
			if key == '1':
				global SETTINGS
				getSettings()
				SETTINGS['mask'] = selected
				saveJson(SETTINGS, confName)
				
				getSettings()
				saveCfile()

				if os.path.exists(goodPath):
					print('remove old folder', goodPath)
					shutil.rmtree(goodPath)
				shutil.copytree(confPath, goodPath)
				print('copy from', confPath, 'to', goodPath)
				setNxSlip()
			elif key == '2':
				if os.path.exists(goodPath):
					print('remove old folder', goodPath)
					shutil.rmtree(goodPath)
				setNxSlip()
			elif key == '3':
				setPrevSlip()
			else:
				userAbort()
			SHOW_BOTTOM = False
			showChanges()
			return
		else:
			if key == '1':
				print('--------reset data')
				resetData()

			elif key == '3':
				SHOW_MASK = not SHOW_MASK
				print('SHOW_MASK = ', SHOW_MASK)

			elif key == '0':
				cv2.destroyAllWindows()
				'''
				betType	= input('Please input bet type : ')
				raceID	= input('Please input race number or front end ID : ')
				detail	=input('Please input selection detail : ')
				fname = '{}_{}_{}_{}'.format(slipName, betType, raceID, detail)
				'''
				fname = 'slip'
				genSlipData(selected, fname)
				print('--------created ',fname,'.bin')
				exit(0)
			else:
				userAbort()
	showChanges()
#######################################################################
def onTouch(event,x,y,flags,param):
	if  event == cv2.EVENT_RBUTTONUP:
		findSel(x, y)
	elif  event == cv2.EVENT_LBUTTONUP:
		findSel(x, y)
def uiThread():
	global clicked
	if clicked:
		clicked = False
		showChanges()
def mainloop():
	cv2.namedWindow('image')
	cv2.setMouseCallback('image',onTouch)
	while True:
		key = cv2.waitKey(100)
		if key != -1:
			processKey(key)
		uiThread()
	cv2.destroyAllWindows()

def sort2list(lstKey,lstData):
	sortedK = []
	sortedD = []
	inxSrc = 0
	for k in lstKey:
		inxDst = 0
		for s in sortedK:
			if s > k:
				break
			inxDst += 1
		sortedK.insert(inxDst,k)
		sortedD.insert(inxDst,lstData[inxSrc])
		inxSrc += 1
	return sortedK,sortedD
def getSlipIDlist():
	global SETTINGS
	lstID	= []
	lstName	= []
	for root, dirs, files in os.walk(OUT_PATH):
		tmp = root.split('\\')
		if len(tmp) > 1:
			slip_name = tmp[1]
			requireFiles = [r'SETTINGS.json', r'betSlip.bmp']
			for f in requireFiles:
				name = os.path.join(root, f)
				if not os.path.exists(name):
					print(name, ' not exist')
					break
			else:
				confName = os.path.join(root, r'SETTINGS.json')
				with open(confName, 'r', encoding='utf-8') as f:
					SETTINGS = json.load(f)
				slipID	= SETTINGS['slipID']
				lstID.append(slipID)
				lstName.append(slip_name)
	if len(lstID) == 0:
		abort('no valid slip')

	lstID, lstName = sort2list(lstID, lstName)
	retID	= []
	retName	= []
	i = 0
	for ID in lstID:
		if ID in retID:
			x = retID.index(ID)
			retName[x].append(lstName[i])
		else:
			retID.append(ID)
			retName.append([lstName[i]])
		i += 1

	fpLst = codecs.open('slip.lst', "w", encoding="utf-8")
	for i in range(len(retID)):
		msg = '{}\t{}\n'.format(retID[i], retName[i])
		fpLst.write(msg)
	fpLst.close()
	return retID, retName, lstName

def getSlipName():
	global slipNames, slipName, slipInx
	try:
		ID = int(slipName)
		if ID in slipIDs:
			slipInx = slipIDs.index(ID)
			names = slipNames[slipInx]
			sz = len(names)
			i = 0
			if sz != 1:
				for i in range(sz):
					print('{:>3d} : {}'.format(i, names[i]))
				key = input('Please select slip (0-{}) : '.format(sz - 1))
				try:
					i = int(key)
				except ValueError as e:
					abort('Invalid selection')
			slipName = names[i]
		else:
			notExistAbort('ID')
	except ValueError as e:
		if not (slipName in lstName):
			notExistAbort('slip name')
	print('Selected Slip = ', slipName)

slipIDs, slipNames, lstName = getSlipIDlist()
print(slipNames)
saveSlipNames()
showSlipNames()
slipName = input("Please select slip (ID or Name) or 0 for BROWSE: ")
if slipName == '0':
	slipName = input("Start which slip : ")
	slipInx = 0
	if slipName != '0':
		getSlipName()
	slipInx -= 1
	setNxSlip()
	MODE = 'BROWSE'
	SHOW_MASK = True
	print('1 = save change')
	print('2 = skip change')
	print('3 = previous skip')
else:
	getSlipName()
	getSettings()
	resetData()
	MODE = ''
	SHOW_MASK = False
	print('0 = save data')
	print('1 = reset data')
	print('3 = HOW_MASK')
SHOW_BOTTOM = False
print('4 = show lower part of slip')
print('5 = show upper part of slip')
print('other = abort')
mainloop()

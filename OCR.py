#!/usr/bin/python
# -*- coding: UTF-8 -*-
SLIP_NAME	= ''			#'' = all pdf in ./pdf
ROTATION	= 0
BOXED_CELL	= False

def adj4slipType():
	global spaceWsel, spaceHsel
	global rightSelAdj, bottomSelAdj
	global shapeSel
	if BOXED_CELL:
		spaceWsel	= 80.4		#horizontal distnnce between selectable cell
		spaceHsel	= 80.5		#vertical distnnce between selectable cell
		rightSelAdj	= 78		#distance of selectable area from right edge of bet slip
		bottomSelAdj= 134		#distance of selectable area from bottom edge of bet slip
		shapeSel	= [67,66]
	else:
		spaceWsel	= 39.3333	#horizontal distnnce between selectable cell
		spaceHsel	= 55.0		#vertical distnnce between selectable cell
		rightSelAdj	= 78		#distance of selectable area from right edge of bet slip
		bottomSelAdj= 99		#distance of selectable area from bottom edge of bet slip
		shapeSel	= [23,8]
	global leftSel, topSel
	leftSel= 74
	topSel = 115			
	global shapeDim1, shapeDim, shapeMarker, shapeID
	shapeDim1	= [24,24]
	shapeDim	= [16,16]
	shapeMarker	= [22,22]
	shapeID		= [8,22]
	global spaceWid, spaceHid, bottomIDadj
	spaceWid	= 20		#width of ID area
	spaceHid	= 54.714	#vertical distnnce between ID marker
	bottomIDadj	= 210		#distance of ID area from bottom edge of bet slip

import sys
import time
import traceback
import glob
import json
import os
import shutil
import codecs
import numpy as np
import copy
import cv2
import imutils
#from google.colab.patches import cv2_imshow

#conda install -c conda-forge poppler
#!sudo apt-get install -y poppler-utils
#!pip install pdf2image
from pdf2image import convert_from_path

class MyError(Exception):
	# Constructor or Initializer
	def __init__(self, value):
		self.value = value
	# __str__ is to print() the value
	def __str__(self):
		return(self.value)
def saveLog(msg):
	global fpLOG
	print(msg)
	fpLOG.write(msg + '\n')
def saveError(msg):
	saveLog(slipName + ' ' + msg)
	raise(MyError(msg))

def deleteFiles(path):
	files = glob.glob(path)
	for f in files:
	    try:
	        os.remove(f)
	    except OSError as e:
	        print("Error: %s : %s" % (f, e.strerror))

def saveImg(fname,img):
	print('saveImg = ',fname,img.shape)
	cv2.imwrite('tmp.bmp', img)
	shutil.copy2('tmp.bmp', fname)
def showImg(fname,img):
	print('showImg = ',fname,img.shape)
	cv2.imwrite(fname, img)
#################################################################################
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
def prnTable(m):
	for r in m:
		for i in r:
			print("{:>3d}".format(i), end=',')
		print()
def prnShape(lstS,lstC):
	i = 0
	for s in lstS:
		print('{:>2d}----{:>3d}[{:>3d},{:>3d}] ,'.format(i,len(lstC[i]),s[0],s[1]),lstC[i])    
		i += 1
def sort2list(lstKey,lstData):
	sortedK = []
	sortedD = []
	inxSrc = 0
	for k in lstKey:
		inxDst = 0	
		for s in sortedK:
			if s < k:
				break
			inxDst += 1
		sortedK.insert(inxDst,k)
		sortedD.insert(inxDst,lstData[inxSrc])
		inxSrc += 1
	return sortedK,sortedD
def prnDataSrc(lstKey,lstData):
	keys = copy.deepcopy(lstKey)
	lst = copy.deepcopy(lstData)
	keys,lst = sort2list(keys,lst)
	i = 0
	for k in keys:
		if i % 10 == 0:
			print()
			print('{:>3d} ::  '.format(i), end='')
		print(k, lst[i])	#, end = '\t')
		i += 1
	print()		
	print()	
########################################################################################
def setBGcolor(img, color):
	#return np.full((h, w, 3), color, np.uint8)
	img[:] = color	#(0, 0, 255)
	return img	
def genBlackBG8mask(binImg):
	h, w = binImg.shape
	return np.zeros((h, w, 3), np.uint8)
def genWhiteBG8img(img):
	return np.copy(img) * 255
def genBlackBG8img(img):
	return np.copy(img) * 0

def prnColor(x, y, img, binImg):
	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)		
	W = 10
	H = 10
	x -= int(W/2)
	y -= int(H/2)
	print('prnColor', x, y, W, H)
	for j in range(H):
		y1 = y + j
		for i in range(W):
			x1 = x + i
			print(binImg[y1][x1], hsv[y1][x1], end = ', ')
		print()
	exit(0)
def genBinImgColor(img,min,max):
	hsvOrg = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)		
	lower = np.array(min)		
	upper = np.array(max)
	return cv2.inRange(hsvOrg, lower, upper)
def genBinImgGray(img, blockSize, C):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blockSize, C)
def genBinImgGray1(img):
	return genBinImgGray(img, 21, 4)
def genBinImgGray2(img):
	return genBinImgGray(img, 15, 10)

def genBinImgBlack(img):
#	binImg = genBinImgColor(img, [110, 0, 25], [160, 125, 50])
	binImg = genBinImgColor(img, [0, 0, 0], [160, 125, 50])
#	prnColor(1670, 422, img, binImg)
	return binImg
def genBinImgBlack1(img):
	binImg = genBinImgColor(img, [0, 0, 0], [5, 5, 5])
#	prnColor(247, 802, img, binImg)
	return binImg
def genBinImgBlack2(img):
	binImg = genBinImgColor(img, [130, 0, 160], [140, 5, 170])
#	prnColor(901, 209, img, binImg)
	return binImg
def genBinImgGreen(img):
	binImg = genBinImgColor(img, [130,250,220], [150,255,240])
#	prnColor(172,441, img, binImg)
	return binImg
def genBinImgGreen1(img):
	binImg = genBinImgColor(img, [35,250,155], [55,255,175])
#	prnColor(172,441, img, binImg)
	return binImg
########################################################################################
def getXaxis(coords):	#0/1 = by row/col
	Xaxis = []
	lstYs = []
	if len(coords) > 0:
		coords.sort(key=lambda x : x[0])
		oldX = coords[0][0]
		Ys = [coords[0][1]]
		for coord in coords[1:]:
			x = coord[0]
			y = coord[1]
			if abs(x - oldX) > 2:
				Xaxis.append(oldX)
				oldX = x
				Ys.sort()
				lstYs.append(Ys)
				Ys = []
			Ys.append(y)
		Xaxis.append(oldX)
		Ys.sort()
		lstYs.append(Ys)
	return Xaxis,lstYs

def getObjects(binImg, fName):
	bg = genBlackBG8mask(binImg)
	contours, hierarchy = cv2.findContours(binImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	objects = []
	for contour in contours:
		d = cv2.boundingRect(contour)
		objects.append(d)
		x,y,w,h = d
		cv2.rectangle(bg,(x,y),(x+w,y+h),(0,255,0),2)
	showImg(fName, bg)
	return objects
def getObjectInZone(objects,zone):
	left,top,right,bottom = zone
	print('getObjectInZone', zone)
	retObj = []
	for obj in objects:
		x,y,w,h = obj
		if x > left and y > top and x + w < right and y + h < bottom:
			retObj.append(obj)
	return retObj

def isSameShape(obj1, obj2):
	if abs(obj1[0] - obj2[0]) < 2 and abs(obj1[1] - obj2[1]) < 2:
		return True
	return False
def isSameShape2(obj1, obj2):
	if abs(obj1[0] - obj2[0]) <= 2 and abs(obj1[1] - obj2[1]) <= 2:
		return True
	return False
def getShapes(objects):
	lstS = []
	lstC = []
	for obj in objects:
		coord = obj[:2]
		shape = obj[2:]
		i = 0
		for s in lstS:
			if isSameShape(shape, s):
				break;
			i += 1           
		else:
			lstS.append(shape)
			lstC.append([])
		lstC[i].append(coord)
	lstS,lstC = sort2list(lstS,lstC)
	print('getShapes :: ')
	prnShape(lstS,lstC)
#	prnDataSrc(lstS,lstC)
	return lstS,lstC
def findShape(lstS, shape):
	found = []
	i = 0
	for s in lstS:
		if isSameShape2(shape, s):
			found.append(i)
		i += 1
	print('found = ', found)		
	return found
########################################################################################		
def isGoodPattern(pattern):
	ref = int(pattern[0][0])
	for row in pattern:
		for e in row:
			if abs(ref - int(e)) >= 3:
				return True
	return False
def matchPatten(binImg, pattern, threshold, name):
	coords = []
	if isGoodPattern(pattern):
		bg = genBlackBG8mask(binImg)
		w, h = pattern.shape[::-1]
		res = cv2.matchTemplate(binImg, pattern, cv2.TM_CCOEFF_NORMED)
		loc = np.where(res >= threshold)
		for pt in zip(*loc[::-1]):
			coords.append(pt)
			cv2.rectangle(bg, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
		showImg(name, bg)
	return coords

def isMarker(x, y, binImg):
	marker = binImg[y : y + shapeMarker[1] - 2, x : x + shapeMarker[0] - 2]
	return np.all(marker == 255)
def getMarker(lstS, lstC, binImg):
	found = findShape(lstS,shapeMarker)
	coords = []
	for i in found:
		print(i, lstC[i])
		coords += lstC[i]
	lenC = len(coords)
	for i in range(lenC - 1):
		oldX, oldY = coords[i]
		for coord in coords[i + 1:]:
			if (abs(oldY-coord[1]) <= 2):
				l = oldX
				r = coord[0]
				if l > r:
					tmp = l
					l = r
					r = tmp
				if r - l > 200:
					if isMarker(oldX, oldY, binImg) and isMarker(coord[0], coord[1], binImg):
						print('marker = ', oldY, l, r)
						return oldY, l, r
	saveError('shapeMarker error {}'.format(found))

def getIDcoords(img, name):
	imgBlack = genBinImgBlack(img)
	objectsBlack = getObjects(imgBlack, name) 
	lstS,lstC = getShapes(objectsBlack)
	markerY, markerL, markerR = getMarker(lstS, lstC, imgBlack)
	found = findShape(lstS, shapeID)
	coords = []
	for inxID in found:
		coords += lstC[inxID]
	if coords == []:
		saveError('shapeID error, no coords, {} {}'.format(found, shapeID))
	Xaxis, lstYs = getXaxis(coords)
	prnDataSrc(Xaxis, lstYs)
	R = markerR + shapeMarker[0]
	T = markerY - bottomIDadj - (8 * spaceHid)		#- 600
	Xs = []
	Ys = []
	for i in range(len(Xaxis)):
		x = Xaxis[i]
		lstY = []
		for y in lstYs[i]:
			if (y < markerY) and (y > T):
				lstY.append(y)
		if len(lstY) <= 0:
			continue
		if ((x < R) and (x > markerR)) or ((len(Xaxis) == 1) and (len(lstY) > 1)):
			Xs.append(x)
			Ys.append(lstY)
	print(Xs, Ys)
	if len(Xs) != 1:
		saveError('shapeID error')
	xID = Xs[0]
	print('getIDcoords = ', xID, Ys[0])
	return xID, Ys[0]

def getDimension8marker(coords, shape):
	lenR = len(coords)
	for lt in range(lenR - 3):
		for lb in range(lt + 1, lenR):
			if (abs(coords[lt][0] - coords[lb][0]) <= 2):
				for rt in range(lt + 1, lenR):
					if (abs(coords[lt][1] - coords[rt][1]) <= 2):
						for rb in range(lt + 1, lenR):
							if (lb != rb) and (rt != rb) and (rt != lb):
								if (abs(coords[lb][1] - coords[rb][1]) <= 2) and (abs(coords[rt][0] - coords[rb][0]) <= 2):
									l = coords[lt][0]
									r = coords[rb][0]
									if l > r:
										tmp = l
										l = r
										r = tmp
									t = coords[lt][1]
									b = coords[rb][1]
									if t > b:
										tmp = t
										t = b
										b = tmp
									if ((r - l) > 100) and ((b - t) > 100):
										d = shape[0] / 2
										l = int(l + d + 0.5)                    
										t = int(t + d + 0.5)                     
										r = int(r + d + 0.5)                     
										b = int(b + d + 0.5)
										print('getDimension8marker = ', l,t,r,b)
										return l, t, r, b
	print(slipName, 'getDimension8marker error', shape)
	return -1,-1,-1,-1
def getDimension8markerAll(binImg, shape, fname, zone):
	objects = getObjects(binImg, fname) 
	objects = getObjectInZone(objects, zone)
	lstS,lstC = getShapes(objects)
	found = findShape(lstS, shape)
	for i in found:
		l, t, r, b = getDimension8marker(lstC[i], shape)
		if l >= 0:
			return l, t, r, b
	return -1,-1,-1,-1

def getDimension8pattern(binImg, zone):
	cross = np.array([
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255		],
	[	255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255		],
	[	255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255		],
	[	255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255		],
	[	255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255		],
	[	255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		],
	[	  0,  0,  0,  0,  0,255,255,255,255,255,255,  0,  0,  0,  0,  0		]	], np.uint8)
	h,w = cross.shape
	left,top,right,bottom = zone
	coords = matchPatten(binImg, cross, 0.72, 'matchedCross.bmp')
	print(coords)
	ret = []
	for c in coords:
		x, y = c
		if x > left and y > top and x + w < right and y + h < bottom:
			for r in ret:
				if (abs(c[0] - r[0]) <= 2) and (abs(c[1] - r[1]) <= 2):
					break
			else:
				ret.append(c)
	print(ret)
	if len(ret) < 4:
		print(slipName, 'getDimension8pattern not found', cross.shape, zone)
		return -1,-1,-1,-1
	return getDimension8marker(ret, [w, h])
def getDimension8rect(binImg,zone):
	objects = getObjects(binImg, 'maskRect.bmp')
	objects = getObjectInZone(objects, zone)
	lstS,lstC = getShapes(objects)
	if len(lstC) > 0:
		w, h = lstS[0]
		l, t= lstC[0][0]
		r = l + w
		b = t + h
		if (w > 100) and (h > 100):
			print('getDimension8rect = ', l,t,r,b)
			return l, t, r, b
	print(slipName, 'getDimension8rect not found')
	return -1,-1,-1,-1
def getDimension8shortLine(binImg,zone):
	objects = getObjects(binImg, 'maskRect.bmp')
	l, t, r, b = zone
	l -= 100
	r += 70
	b += 80
	zone = [l, t, r, b]
	objects = getObjectInZone(objects, zone)
	lstS,lstC = getShapes(objects)
	if (len(lstS) != 2) or (len(lstC[0]) != 4) or (len(lstC[1]) != 4):
		print(slipName, 'getDimension8shortLine not found', zone)
		return -1,-1,-1,-1
	r = lstC[1][0][0]
	b = lstC[0][0][1]
	l = lstC[1][3][0]
	t = lstC[0][3][1]
	print('getDimension8shortLine = ', l,t,r,b)
	return l, t, r, b

def getDimension(img):
	imgBlack = genBinImgBlack(img)
	objectsBlack = getObjects(imgBlack, 'maskBlackOrg.bmp')
	lstS,lstC = getShapes(objectsBlack)

	markerY, markerL, markerR = getMarker(lstS, lstC, imgBlack)
	xID, YsID = getIDcoords(img, 'maskBlackOrg.bmp')
	found = findShape(lstS,shapeID)

	H, W, c = img.shape
	dimL = markerL - 44
	dimT = 0
	dimR = xID
	if dimR < markerR:
		dimR = markerR
	dimR += 66
	dimB = markerY + 66
	print('zoneDim = ', dimL, dimT, dimR, dimB, W, H)
	if (dimB + 4 > H) and (dimL - 4 < 0):
		if (dimR + 4 > W):
			b, r, c = img.shape
			print(slipName, 'getDimension autual size', r, b)
			return 0, 0, r, b

	dimL -= shapeDim[0] + 2
	if dimL < 0:
		dimL = 0
	dimR += shapeDim[0] + 2		
	dimB += shapeDim[1] + 2
	zoneDim = [dimL, dimT, dimR, dimB]
	print('zoneDim = ', dimL, dimT, dimR, dimB)

	if BOXED_CELL:
		binImgRed = genBinImgGray1(img)
		l, t, r, b = getDimension8rect(binImgRed,zoneDim)		
		if l >= 0:
			l += 6
			t += 6
			r -= 6
			b -= 6
			return l, t, r, b
	else:
		l, t, r, b = getDimension8markerAll(imgBlack, shapeDim, 'maskBlackOrg.bmp', zoneDim)
		if l >= 0:
			return l, t, r, b
		l, t, r, b = getDimension8markerAll(imgBlack, shapeDim1, 'maskBlackOrg.bmp', zoneDim)
		if l >= 0:
			return l, t, r, b

		imgBlack1 = genBinImgBlack1(img)
		showImg('maskBlackOrg1.bmp', imgBlack1)
		l, t, r, b = getDimension8shortLine(imgBlack1, zoneDim)
		if l >= 0:
			return l, t, r, b
		
		imgBlack2 = genBinImgBlack2(img)
		l, t, r, b = getDimension8markerAll(imgBlack2, shapeDim, 'maskBlackOrg2.bmp', zoneDim)
		if l >= 0:
			return l, t, r, b
			
		l, t, r, b = getDimension8pattern(imgBlack, zoneDim)
		if l >= 0:
			return l, t, r, b
		
		imgGreen = genBinImgGreen(img)
		showImg('maskGreenOrg.bmp', imgGreen)
		l, t, r, b = getDimension8rect(imgGreen, zoneDim)
		if l >= 0:
			return l, t, r, b
		
		imgGreen1 = genBinImgGreen1(img)
		showImg('maskGreen1Org.bmp', imgGreen1)
		l, t, r, b = getDimension8rect(imgGreen1, zoneDim)
		if l >= 0:
			return l, t, r, b
	saveError('getDimension not found1')
########################################################################################		
def getOrgImg(orgName):
	print('orgName = ', orgName)
	img = cv2.imdecode (np.fromfile (orgName, dtype = np.uint8), -1)	#img = cv2.imread(orgName)
	if ROTATION == 90:
		img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)	
	elif ROTATION == 180:
		img = cv2.rotate(img, cv2.ROTATE_180)	
	elif ROTATION == 270:
		img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
	showImg('rotate.bmp', img)		
	return img
def cropImage(img, name):
	l, t, r , b = getDimension(img)
	cropped = img[t:b,l:r] 
	saveImg(name, cropped)
	return cropped

def getRegionSel():
	global rightSel,bottomSel, leftSel, topSel
	global zoneSel
	l = int(rightSel - (spaceWsel * slipCol))
	if l < 0:
		l = 0
	t = int(bottomSel - (spaceHsel * slipRow))
	if t < 0:
		t = 0
	if (leftSel != l) or (topSel != t):
		print('slip-',slipName, ' :: leftSel or topSel will be incorrect',leftSel, l, topSel, t)
		topSel	= t
		leftSel	= l
	zoneSel= [leftSel,topSel,rightSel,bottomSel]

def getRegions():
	global rightID, bottomID, leftID, topID
	global rightSel,bottomSel, leftSel, topSel
	global slipCol,slipRow

	cropH,cropW,cropC	= cropImg.shape
	rightSel = cropW - rightSelAdj
	bottomSel= cropH - bottomSelAdj
	w = rightSel - leftSel
	h = bottomSel - topSel
	slipCol = int(w / spaceWsel + 0.5)
	slipRow = int(h / spaceHsel + 0.5)
	getRegionSel()

	bottomID= cropH - bottomIDadj
	leftID= int(rightID - spaceWid)
	topID = int(bottomID - (spaceHid * 8))

def drawGrid(img,l,t,r,b,spW,spH):
	color = (255,0,0)
	thickness = 1
	x = l
	while x <= r + 1:
		x1 = int(x + 0.5)
		cv2.line(img, (x1,t), (x1,b), color, thickness)
		x += spW
	y = t
	while y <= b + 1:
		y1 = int(y + 0.5)
		cv2.line(img, (l,y1), (r,y1), color, thickness)
		y += spH
def drawGridSel(cropImg):
	img = cropImg.copy()
	drawGrid(img, leftSel,topSel,rightSel,bottomSel,spaceWsel,spaceHsel)
	drawGrid(img, leftID,topID,rightID,bottomID,spaceWid,spaceHid)
	print('leftID,topID,rightID,bottomID,spaceWid,spaceHid----',leftID,topID,rightID,bottomID,spaceWid,spaceHid)
	showImg('cropGrid.bmp', img)
	global imgCropGrid
	imgCropGrid = img

def getIndex(x,end,space,cnt):
	if x >= end:
		return -1
	for i in range(cnt + 1):
		pos = end - int(space * (i + 1))
		if x > pos:
			return cnt - i - 1
	return -2
def getID(x, Ys):
	global rightID,spaceWid, bottomID,spaceHid
	lstID = [0] * 8
	for y in Ys:
		c = getIndex(x,rightID,spaceWid,1)
		r = getIndex(y,bottomID,spaceHid,8)
		if c >= 0 and r >= 0:
			lstID[r] = 1
	ret = 0			
	i = 1
	for e in lstID:
		if e != 0:
			ret += i
		i <<= 1			
	return ret
#############################################################################
def getCoordsSel(binImg, shape, name):
	print('....................getCoordsSel getObjectInZone')
	obj = getObjects(binImg, name)
	objSel = getObjectInZone(obj,zoneSel)

	lstS,lstC = getShapes(objSel)
	print('....................getCoordsSel findShape')
	found = findShape(lstS, shape)
	coords = []
	for i in found:
		coords += lstC[i]
	print('getCoordsSel findShape = ', found, coords)
	return coords

def getCellPattern(coords, binImg):
	global shapeSel
	Xaxis,lstYs = getXaxis(coords)
	print('.................Xaxis')
#	prnDataSrc(Xaxis,lstYs)
	for col in range(len(Xaxis)):
		lst = lstYs[col]
		row = 0
		while row < len(lst) - 1:
			distance = abs(lst[row] - lst[row + 1])
			if abs(distance - 36) <= 2:
				if row < len(lst) - 2:
					distance = abs(lstYs[col][row] - lstYs[col][row + 2])
					if distance + 2 < spaceHsel:
						row += 1
						continue
				break
			row += 1
		else:								
			col += 1
			continue
		break				
	else:
		saveError('up/down arrow error, not enough data {}'.format(lstYs[0]))

	l = Xaxis[col]
	t = lstYs[col][row]
	r = l + shapeSel[0]
	b = t + shapeSel[1] - 1
	arrowUp = binImg[t:b,l:r] 
	l = Xaxis[col]
	t = lstYs[col][row + 1] + 1
	r = l + shapeSel[0]
	b = t + shapeSel[1]
	arrowDn = binImg[t:b,l:r]

	showImg('arrowUp.bmp', arrowUp)
	showImg('arrowDn.bmp', arrowDn)
	return arrowUp, arrowDn

def Y2row(Ys):
	Ys.sort()        
	oldY = Ys[0]
	row = [oldY]
	for y in Ys[1:]:
		if abs(oldY-y) >= 2:
			row.append(y)
		oldY = y        
	return row
def cutNonCell(lstData):
	m = []
	for Ys in lstData:
		row = Y2row(Ys) 
		m.append(row)	
	return m

def genEmptyMatrix(col,row):
	return [[0 for x in range(col)] for y in range(row)]
def genEmptyMask():
	return genEmptyMatrix(slipCol,slipRow)
def getInx(x,end,space,cnt):
	if x < end:
		for i in range(cnt + 1):
			pos = end - int(space * (i + 1))
			if x > pos:
				return cnt - i - 1
	return -1
def getMask(Xaxis,lstYs):
	lstData = cutNonCell(lstYs)
	lstYs = lstData

	table = genEmptyMask()
	i = 0
	for x in Xaxis:
		c = getIndex(x,rightSel,spaceWsel,slipCol)
		if c < 0:
			print('get Mask fail to get X = ', i)
			break
		j = 0		
		Ys = lstYs[i]
		Ys.sort()
		for y in Ys:			
			r = getIndex(y,bottomSel,spaceHsel,slipRow)
			if r < 0:
				print('get Mask fail to get Y = ', j)
				break
			table[r][c] = 1		
			j += 1							
		i += 1
	return table
def getMask8pattern(binImg, pattern, threshold, name):
	global slipCol, rightSel
	coords = matchPatten(binImg, pattern, threshold, name)
	Xaxis,lstYs = getXaxis(coords)
	r = zoneSel[2] - int(shapeSel[1] + (spaceWsel - shapeSel[1]) / 2)
	l = Xaxis[0]
	if leftSel > l:
		print('!!!!',l,leftSel)
		slipCol = int(((r - l) / spaceWsel) + 1.5)
	if abs(r - Xaxis[-1]) > 12:
		print('????',r,Xaxis[-1])
		rightSel = int(Xaxis[-1] + shapeSel[1] + (spaceWsel - shapeSel[1]) / 2)
		getRegionSel()
	return getMask(Xaxis, lstYs), rightSel
########################################################################################
def inverseMask(mask):
	m = []
	for row in mask:
		lst = []
		for e in row:
			lst.append(e ^ 1)
		m.append(lst)  
	return m      
def drawContours(contours, binImg):
	bg = genBlackBG8mask(binImg)
	i = 0
	for approx in contours:
		color = (255,0,128)
		if i & 1 != 0:
			color = (0,0,255)
		color = (255, 255, 255)
		cv2.drawContours(bg, [approx], -1, color, 1, lineType = cv2.LINE_AA)
		M = cv2.moments(approx)
		if M['m00'] != 0.0:
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])
			if i & 1 != 0:
				y += 20
			cv2.putText(bg, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
		i += 1
	showImg('frame.bmp', bg)
	showImg('frameRef.bmp',binImg)
def getErrorPt(approx):
	errorX = np.zeros(len(approx), dtype=int)
	errorY = np.zeros(len(approx), dtype=int)
	beg = approx[-1]
	i = 0
	for c in approx:
		if (abs(c[0][0] - beg[0][0]) > 2):
			errorX[i] = 1
		if (abs(c[0][1] - beg[0][1]) > 2):
			errorY[i] = 1
		beg = c
		i += 1
	return errorX, errorY
def deletePoint(approx, mark):
	ret = approx
	x = np.where(mark)
	a = np.flipud(x[0]) 
	for i in a:
		ret = np.delete(ret, i, axis=0)
	return ret
def getChanges(errorX)	:
	error = np.delete(errorX, 0)
	error = np.append(error, errorX[0])
	error = np.logical_xor(error, errorX)
	error = np.logical_or(error, errorX)
	return np.logical_not(error)
def deleteOverlapPt(approx):
	errorX, errorY = getErrorPt(approx)
	errorX = getChanges(errorX)
	errorY = getChanges(errorY)
	x = np.where(errorX)
	for i in x[0]:
		if (abs(approx[i - 1][0][1] - approx[(i + 1) % len(x[0])][0][1]) <= 2):
			errorX[i] = False
	x = np.where(errorY)
	for i in x[0]:
		if (abs(approx[i - 1][0][0] - approx[(i + 1) % len(x[0])][0][0]) <= 2):
			errorY[i] = False
	error = np.logical_or(errorX, errorY)
	return deletePoint(approx, error)
def approx2frame(approx):
	errorX, errorY = getErrorPt(approx)
	error = np.logical_and(errorX, errorY)
	mark = error
	x = np.where(error)
	for i in x[0]:
		if (abs(approx[i - 2][0][0] - approx[i][0][0]) <= 2) or (abs(approx[i - 2][0][1] - approx[i][0][1]) <= 2):
			mark[i-1] = 1
			mark[i] = 0
	ret = deletePoint(approx, mark)
#	ret = deleteOverlapPt(ret)
	return ret

def getTableLines(binImg, mask):
	cells = np.array(mask)
	row = np.any(cells != 0, axis = 1)
	col = np.any(cells != 0, axis = 0)
	r = np.argmax(row == True)
	c = np.argmax(col == True)
	left = leftSel+ int((c - 0.5) * spaceWsel) 
	top = topSel + int((r - 0.5) * spaceHsel) 
	right = rightSel + int(0.5 * spaceWsel) 
	bottom = bottomSel+ int(0.5 * spaceHsel) 
	minArea = spaceHsel * spaceWsel

	contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	objects = []
	for i in range(len(contours)):
		area = cv2.contourArea(contours[i])
		approx = cv2.approxPolyDP(contours[i], epsilon = 10, closed=True )
		if (area > minArea) and (len(approx) >= 4) and (approx[0][0][0] > left) and (approx[0][0][1] > top):
			ret = approx2frame(approx)
			x,y,w,h = cv2.boundingRect(ret)
			if (x > left) and (y > top) and (x + w < right) and (y + h < bottom):
				objects.append(ret)
	drawContours(objects, binImg)
#	bg = genBlackBG8mask(binImg)
#	cv2.drawContours(bg, contours, -1, (255,255,255), 1, lineType = cv2.LINE_AA)
#	showImg('00.bmp',bg)
	return objects

'''
	-1	-2
	3----2		10	3	3	9		 4
	|10	9|		12			12		1 2
	|6	5|12	12			12		 8
	0----1		6	3	3	5
	  3
		beg			end
		y					y
		B<E	B>E				B<E	B>E
x		8	4		x		4	8	
B<E	2				B<E	1
B>E	1				B>E	2
'''		
def getIndexline(pt):
	global rightSel, spaceWsel, slipCol
	newRight = int(rightSel + (spaceWsel / 2))
	c = getIndex(pt[0][0], newRight, spaceWsel, slipCol + 1)
	global bottomSel, spaceHsel, slipRow
	newBottom = int(bottomSel + (spaceHsel / 2))
	r = getIndex(pt[0][1], newBottom, spaceHsel, slipRow + 1)
	return r, c
def getLineDir(beg, end):
	dir = 2
	if beg > end:
		dir = 1
		tmp = beg
		beg = end
		end = tmp
	return beg, end, dir
def genEmptyTableLine():
	tableLine = genEmptyMatrix(slipCol + 1, slipRow + 1)
	npTable = np.asarray(tableLine)
	npTable[:,0] = 12
	npTable[0] = 3
	npTable[:,-1] = 12
	npTable[-1] = 3
	npTable[0][0] = 10
	npTable[0][-1] = 9
	npTable[-1][0] = 6
	npTable[-1][-1] = 5
	ret = npTable.tolist ()
	return ret
	
def obj2tableLine(binImg, mask):
	objects = getTableLines(binImg, mask)
	if len(objects) == 0:
		saveLog('getTableLines no objects')
		return genEmptyTableLine()
	tableLine = genEmptyMatrix(slipCol + 1, slipRow + 1)
	'''
	k = 0
	old = tableLine[9][18]
	'''
	for approx in objects:
		errorX, errorY = getErrorPt(approx)
		for i in range(len(approx) - 1, -1, -1):
			r1, c1 = getIndexline(approx[i])
			r2, c2 = getIndexline(approx[i - 1])
			if (r1 == r2) and (c1 == c2):
				continue
			if not errorY[i]:
				pt1, pt2, dir = getLineDir(c1, c2)
				chB = dir
				chE = chB ^ 3
				for c in range(pt1 + 1, pt2):
					tableLine[r1][c] |= 3
			elif not errorX[i]:
				pt1, pt2, dir = getLineDir(r1, r2)
				chB = dir << 2
				chE = chB ^ 12
				for r in range(pt1 + 1, pt2):
					tableLine[r][c1] |= 12
			else:
				print(i,r1,c1,r2,c2,errorX[i],errorY[i])
				continue
				
			tableLine[r1][c1] |= chB
			tableLine[r2][c2] |= chE
			'''
			cur = tableLine[9][18]
			if old != cur:
				print(k, i, old, cur, r1, c1, r2, c2)
				if tableLine[9][18] == 14:
					for pt in approx:
						r1, c1 = getIndexline(pt)
						print(r1, c1, pt)
					prnTable(tableLine)
					exit(0)
				old = cur
			'''
		'''
		cur = tableLine[9][18]
		if old != cur:
			print(k, old, cur, approx)
			if tableLine[9][18] == 14:
				prnTable(tableLine)
				exit(0)
			old = cur
		k += 1
		'''
	return tableLine
def cutUnusedLines(tableLine, mask):
	npMask = np.asarray(mask)
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
#######################################################################
def chkCropImg():
	img = genBinImgGray1(cropImg)
	showImg('00.bmp', img)
	skeleton = imutils.skeletonize(img, size=(3, 3))
	showImg('00x.bmp', skeleton)

	maskC = imutils.auto_canny(cropImg)
	showImg('00b.bmp', maskC)
	skeleton = imutils.skeletonize(maskC, size=(3, 3))
	showImg('00y.bmp', skeleton)

def genConf(orgName,cName,cropName, confName):
	global orgImg
	orgImg = getOrgImg(orgName)
	global cropImg
	cropImg = cropImage(orgImg, cropName)
	xID, YsID = getIDcoords(cropImg, 'maskBlackCrop.bmp')
	global rightID
	rightID = xID + shapeID[0] + 5
	getRegions()
	global SETTINGS
	SETTINGS['rightLine'] = rightSel

	global slipID
	slipID = getID(xID, YsID)
	drawGridSel(cropImg)
	binImgRed = genBinImgGray1(cropImg)
	binImgBlack = genBinImgBlack(cropImg)
	invImgBlack = cv2.bitwise_not(binImgBlack)
	img = cv2.bitwise_and(binImgRed, binImgRed, mask= invImgBlack)
	coords	= getCoordsSel(img,	shapeSel, 'maskCell.bmp')
	if len(coords) == 0:
		saveError('find shape not found : {}'.format(shapeSel))

	if BOXED_CELL:
		Xaxis,lstYs = getXaxis(coords)
		maskCell = getMask(Xaxis, lstYs)
		tableLine = genEmptyTableLine()
	else:
		arrowUp, arrowDn = getCellPattern(coords, img)
		mask1, r1 = getMask8pattern(img, arrowUp, 0.7, 'matchedCell1.bmp')
		mask2, r2 = getMask8pattern(img, arrowDn, 0.7, 'matchedCell2.bmp')
		if abs(r1 - r2) > 4:
			saveError('getMask8pattern mask1 or mask2 missing columns')
		np1 = np.array(mask1)
		np2 = np.array(mask2)
		print(np1.shape, np2.shape)
		if np1.shape < np2.shape:
			print('String left of betslip fate down arroe', np1.shape, np2.shape)
#			np2 = np.delete(np2,0,1)
#			np2[:,0] = 0
			np1 = np.insert(np1, 0, np2[:,0], axis=1)
		npCell = np.logical_or(np1, np2)
		obj = getObjects(binImgBlack, 'maskDel.bmp')
		objSel = getObjectInZone(obj,zoneSel)
		lstS,lstC = getShapes(objSel)
		for s in lstS:
			w, h = s
			if (h >= 30) and (h < spaceHsel) and (w >= 3) and (w <= 5):
				print('........  with delete mark', s)
				coordsDel=getCoordsSel(binImgBlack, s, 'maskDel.bmp') 

				Xaxis,lstYs = getXaxis(coordsDel)
				maskDel = getMask(Xaxis, lstYs)
				np1 = np.array(maskDel)
				np1 = np.logical_not(np1)
				npCell = np.logical_and(np1, npCell)
		
		maskCell = npCell.tolist()		
		tableLine = obj2tableLine(genBinImgGray2(cropImg), maskCell)
	SETTINGS['slipID'] = slipID
	SETTINGS['slipCol']	= slipCol
	SETTINGS['slipRow']	= slipRow
	SETTINGS['spaceWsel']	= spaceWsel
	SETTINGS['spaceHsel']	= spaceHsel
	SETTINGS['rightSel']	= rightSel
	SETTINGS['bottomSel']	= bottomSel
	SETTINGS['mask'] = maskCell
	SETTINGS['line'] = tableLine
	saveJson(SETTINGS, confName)

PDF_ORG_PATH = 'pdfOrg\\all'
PDF_270_PATH = 'pdf270'
PDF_180_PATH = 'pdf180'
PDF_90_PATH = 'pdf90'
PDF_BOXED_PATH = 'pdfBox'
PDF_FAIL_PATH = 'pdfFail'
PDF_OK_PATH = 'pdfOK'
PDF_PATH = 'pdf'
IMG_PATH = 'img'
OUT_PATH = 'out'
LOG_NAME = 'slip.log'

def getImgName():
	return '{}\\{}.bmp'.format(IMG_PATH, slipName)		
def saveConfig():
	confPath= '{}\\{}'.format(OUT_PATH, slipName)
	confName= os.path.join(confPath, 'SETTINGS.json')

	if not os.path.exists(confPath):
		os.makedirs(confPath)
	imgName	= getImgName()
	cName	= os.path.join(confPath, 'c.txt')
	cropName= os.path.join(confPath, 'betSlip.bmp')
	src = '{}\\{}.pdf'.format(PDF_PATH, slipName)
	testCases=[	[0, False], [0, True], [90, False], [180, False], [270, False] ]
	for tc in testCases:
		global ROTATION, BOXED_CELL, SETTINGS
		SETTINGS = {}
		if not SLIP_NAME:
			ROTATION, BOXED_CELL = tc
		adj4slipType()
		try:
			deleteFiles('*.bmp')
			genConf(imgName, cName, cropName, confName)
		except MyError as error:
			if SLIP_NAME:
				exit(0)
			elif tc == testCases[-1]:
				print('Error : ', error.value, slipName)
				exit(0)
		except:
			traceback.print_exception(*sys.exc_info())
			exit(0)
		else:
			saveLog('sucessfully created {} (BOXED_CELL = {}, angle = {})'.format(slipName, BOXED_CELL, ROTATION))
			if SLIP_NAME:
				exit(0)
			if BOXED_CELL:
				shutil.copy2(src, PDF_BOXED_PATH)
			elif ROTATION == 90:
				shutil.copy2(src, PDF_90_PATH)
			elif ROTATION == 180:
				shutil.copy2(src, PDF_180_PATH)
			elif ROTATION == 270:
				shutil.copy2(src, PDF_270_PATH)
			else:
				shutil.copy2(src, PDF_OK_PATH)
			return
		finally:
			print("finished", slipName, tc)

def pdf2betslip():
	global slipName
	if SLIP_NAME:
		slipName = SLIP_NAME
		imgName	= getImgName()
		if not os.path.exists(imgName):
			saveError('pdf file not found : ' + imgName)
		saveConfig()
	else:
		successed = 0
		for root, dirs, files in os.walk(IMG_PATH):
			for name in files:
				tmp = name.split(".")
				slipName = tmp[0]
				saveConfig()
				successed += 1
	saveLog('total {} files convertted'.format(successed))
def makePath(path):
	if not os.path.exists(path):
		print('makePath', path)
		os.makedirs(path)
def cleanPath(path):
	if os.path.exists(path):
		print('cleanPath', path)
		shutil.rmtree(path)
	os.makedirs(path)
def copyPath(src, dst):
	if os.path.exists(dst):
		print('copyPath', dst)
		shutil.rmtree(dst)
	shutil.copytree(src, dst)
def pdfConvert(pdfName,name):
	imgName	= '{}\\{}.bmp'.format(IMG_PATH, name)
	if not os.path.exists(imgName):
		print('create bmp : {} from {}'.format(imgName, pdfName))
		shutil.copy2(pdfName, 'tmp.pdf')
		images = convert_from_path('tmp.pdf')
		images[0].save(imgName, 'BMP')
def pdf2bmp():
	deleteFiles('out.txt')
	deleteFiles('*.bin')
	deleteFiles('*.bmp')
	deleteFiles('*.bak')
	if SLIP_NAME:
		makePath(OUT_PATH)
		makePath(IMG_PATH)
		pdfName = '{}\\{}.pdf'.format(PDF_PATH, SLIP_NAME)
		pdfConvert(pdfName, SLIP_NAME)
	else:
		cleanPath(PDF_OK_PATH)
		cleanPath(PDF_FAIL_PATH)
		cleanPath(PDF_BOXED_PATH)
		cleanPath(PDF_90_PATH)
		cleanPath(PDF_180_PATH)
		cleanPath(PDF_270_PATH)
		cleanPath(PDF_FAIL_PATH)
		cleanPath(OUT_PATH)
		cleanPath(IMG_PATH)
		copyPath(PDF_ORG_PATH, PDF_PATH)
		for root, dirs, files in os.walk(PDF_PATH):
			for name in files:
				pdfName = os.path.join(PDF_PATH, name)
				tmp = name.split(".")
				pdfConvert(pdfName, tmp[0])

global fpLOG
fpLOG = codecs.open(LOG_NAME, "w", encoding="utf-8")

pdf2bmp()

pdf2betslip()

fpLOG.close()

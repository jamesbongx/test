#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
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

#####################################################################################
#comboFileType for select file type to be searched 
#pageTable = filter crietrias	: fileTypeLst = file type to be searched 
#	pageTeam					: search in *FBTeam.xml
#	pageTour					: search in *FBTournament.xml
#	pageMatch					: search in *FBMatch.xml
#	pageWagerTour				: search in *FBFOWagering.xml for tournament type pool
#	pageWagerMatch				: search in *FBFOWagering.xml for match type pool
#In pageTeam/pageTour/pageMatch/pageWagerTour/pageWagerMatch, add filter crietrias as follows:
#	'label'	: description of the function of the widget
#	'path'	: XML path to the variable to be search
#	'attr'	: attribute name of the variable to be search
#	'items'	: for combo type only, list of possible value of the variable to be search
#
#pathFO		= path to football XMLs
#pathRace	= path to racing XMLs
#editorPath	= path to notepad++.exe
#####################################################################################	
pathFO = r'C:\ngbt\XML\cmcFootballXmls'
pathRace = r'C:\ngbt\XML\cmcRacingXmls'
editorPath = r'C:\Software\Notepad++\notepad++.exe'
#########################################################################
padLeft			= 5
padTop			= 5
spaceH			= 35
spaceV			= 500
result_width	= 700
window_Left		= 200
window_top		= 50
window_width	= 1400
window_height	= 800
#########################################################################
fileTypeCur = 0
def chgFileType(event):
	global fileTypeCur
	fileTypeCur = ctrlFileType.current()
	top.destroy()
def dispCtrl(combo, y, x):
	ttk.Label(top, text = combo['label']).place(x = x, y = y)
	if 'items' in combo.keys():
		ctrl = ttk.Combobox(top, values = combo['items'], font=('Helvetica', 10))
		if 'action' in combo.keys():
			ctrl.bind('<<ComboboxSelected>>', combo['action'])
	else:
		ctrl = ttk.Entry(top, text = '')
	ctrl.place(x = x + 80, y = y, width = 100, height = 25 ) 
	return ctrl
matchStatus = ["None", "Planning", "MatchDeleted", "ReadyToDefine", "Defined", "PreEvent", "KickedOff", "FirstHalf", "FirstHalfCompleted", "SecondHalf", "FullTimeCompleted", "FirstHalfET", "FirstHalfETCompleted", "SecondHalfET", "SecondHalfETCompleted", "PenaltyKick", "PenaltyKickCompleted", "MatchSuspended", "MatchVoided", "ResultVoided", "InplayResultVoided", "MatchEnded", "InplayMatchEnded"
]	
poolStatus = ["None", "NotReady", "NotOffer", "Cancelled", "ReadyToStartSell", "SellingStarted", "SellingStopped", "Hold", "Suspended", "PayoutStarted", "PayoutStopped", "PayoutHold", "Refund", "RefundBeforeSuspend"
]
pageTeam = [
	{	'label' : 'Team ID',
		'path'	: './Team',
		'attr'	: 'id'
	},
]
pageTour = [
	{	'label' : 'Tour ID',
		'path'	: './Tournament',
		'attr'	: 'tournamentID',
	},
	{	'label' : 'Status',
		'path'	: './Tournament',
		'attr'	: 'st',
		'items' : matchStatus,
	},
]
pageMatch = [
	{	'label' : 'Match ID',
		'path'	: './Match',
		'attr'	: 'matchID'
	},
	{	'label' : 'Status',
		'path'	: './Match',
		'attr'	: 'st',
		'items' : matchStatus,
	},
]
pageWagerTour = [
	{	'label' : 'Pool ID',
		'path'	: './Pool',
		'attr'	: 'id',
	},
	{	'label' : 'Status',
		'path'	: './Pool',
		'attr'	: 'st',
		'items' : poolStatus,
	},
	{	'label' : 'Bet Type',
		'path'	: './Pool',
		'attr'	: 'bTyp',
		'items' : ["TSP", "TQL", "CHP", "GPF", "GPW", "SPC", "TPS", "DHC"],
	},
]
pageWagerMatch = [
	{	'label' : 'Pool ID',
		'path'	: './Pool',
		'attr'	: 'id',
	},
	{	'label' : 'Status',
		'path'	: './Pool',
		'attr'	: 'st',
		'items' : poolStatus,
	},
	{	'label' : 'Bet Type',
		'path'	: './Pool',
		'attr'	: 'bTyp',
		'items' : ["MSP", "CHL", "ECH", "CRS", "ECS", "FCS", "FHA", "FHL", "FTS", "HAD", "EHA", "HDC", "EDC", "HFT", "HHA", "HIL", "EHL", "OOE", "TTG", "ETG", "ETS", "NTS", "ENT", "FGS", "HFM", "ADT", "HCS", "THF", "TOF"],
	},
]
pageTable = [pageTeam, pageTour, pageMatch, pageWagerTour, pageWagerMatch]
comboFileType =	{	
	'label' : 'File Type',
	'items' : ["Team", "Tour", "Match", "wager Tour", "wager Match"],
	'action': chgFileType
}
fileTypeLst = ['FBTeam.xml', 'FBTournament.xml', 'FBMatch.xml', 'FBFOWagering.xml', 'FBFOWagering.xml']
def getFiles8nameFO(filter):
	ret = []
	for rt, dirs, files in os.walk(pathFO):
		for name in files:
			if filter in name:
				ret.append(name)
	return ret
def getXML(fname):
	xmlTree = ET.parse(pathFO + '\\' + fname)
	root = xmlTree.getroot()
	return xmlTree, root
def clickedQuit():
	top.destroy()
	exit(0)
def clickedClean():
	page = pageTable[fileTypeCur]
	for i, ctrl in enumerate(ctrls):
		if 'items' in ctrl.keys():
			ctrl.set('')
		else:
			ctrl.delete(0, 'end')
def clickedSrh():
	page = pageTable[fileTypeCur]
	fnames = getFiles8nameFO(fileTypeLst[fileTypeCur])
	ret = []	
	for fname in fnames:
		xmlTree, root = getXML(fname)
		for i, ctrl in enumerate(ctrls):
			srhValue = ctrl.get()
			if srhValue == '':
				continue
			for elm in root.findall(page[i]['path']):
				if srhValue == elm.attrib[page[i]['attr']]:
					break
			else:
				break
		else:
			ret.append(fname)
	LabelResult.delete(0,'end')
	for fname in ret:
		LabelResult.insert('end', fname)
def showFile(event):
	for i in LabelResult.curselection():
		fname = LabelResult.get(i)
		cmd = editorPath + ' ' + pathFO + '\\' + fname
		print(cmd)
		os.system(cmd)
	print()
	
while True:
	top = tk.Tk()
	top.title('Search XML')
	top.config(bg='#345')
	#top.geometry("600x800+200+50")	
	top.geometry(f'{window_width}x{window_height}+{window_Left}+{window_top}')
	style = ttk.Style()		#(top)
	#style = ttk.Style(top)
	style.configure('.', font=('Helvetica', 10))
	
	butSrh = ttk.Button(top, text = "Search",command = clickedSrh)
	butSrh.place(x = window_width - result_width - 100, y = padTop, width = 70, height = 30)
	
	butClr= ttk.Button(top, text = "Clean",command = clickedClean)
	butClr.place(x = window_width - result_width - 200, y = padTop, width = 70, height = 30)
	
	butQuit= ttk.Button(top, text = "Quit",command = clickedQuit)
	butQuit.place(x = window_width - result_width - 300, y = padTop, width = 70, height = 30)

	LabelResult = tk.Listbox(top)
	LabelResult.place(x = window_width - result_width, y = 0, width = result_width,height = window_height ) 
	LabelResult.bind('<<ListboxSelect>>', showFile)
	
	ctrlFileType = dispCtrl(comboFileType, padTop, padLeft)
	ctrlFileType.current(fileTypeCur)
	
	ctrls = []
	for i, ctrl in enumerate(pageTable[fileTypeCur]):
		y = padTop + (i + 1) * spaceH
		ctrls.append(dispCtrl(ctrl, y, padLeft))
	
	top.mainloop()

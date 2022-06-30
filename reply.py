from datetime import datetime

#############################################	
inData1 = '''0000: 10 00 67 00 42 00 3F 40   ..g.B.?@
0008: 40 40 40 40 33 31 4A 41   @@@@31JA
0010: 4E 31 35 40 40 4D 40 41   N15@@M@A
0018: 53 54 41 30 31 46 45 42   STA01FEB
0020: 31 35 40 20 20 20 20 20   15@     
0028: 20 20 40 20 20 20 20 20     @     
0030: 20 20 41 4B 67 4F 40 60     AKgO@`
0038: 44 40 40 40 40 67 5F 40   D@@@@g_@
0040: 67 5F 40 60 44 40 67 4F   g_@`D@gO
0048: 40 60 40 40 67 5F 40 53   @`@@g_@S
0050: 54 20 53 55 4E 20 52 31   T SUN R1
0058: 30 20 44 2D 54 20 44 45   0 D-T DE
0060: 46 49 4E 45 44 5F 2F      FINED_/
'''
inData2 = '''0000: 10 00 65 00 CA 3D 07 4C   ..e.�=.L
0008: 49 40 31 5B 30 31 46 45   I@1[01FE
0010: 42 31 35 40 40 4D 40 41   B15@@M@A
0018: 53 54 41 30 31 46 45 42   STA01FEB
0020: 31 35 40 20 20 20 20 20   15@     
0028: 20 20 40 20 20 20 20 20     @     
0030: 20 20 41 4B 77 4F 40 70     AKwO@p
0038: 44 40 40 40 40 77 5F 40   D@@@@w_@
0040: 77 5F 40 70 44 40 77 4F   w_@pD@wO
0048: 40 70 40 40 77 5F 40 4D   @p@@w_@M
0050: 4B 36 20 31 35 2F 30 31   K6 15/01
0058: 33 20 53 54 4F 50 20 53   3 STOP S
0060: 45 4C 4C 5D 20            ELL]
'''
def srhDate(hexData):
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
def prnByte(hexData):
	ret = '\\x'.join(hex(x) for x in hexData)
#	print(ret)
	cData = ''
	while len(ret) > 32:
		cData += '"{}"\n'.format(ret[0:32])
		ret = ret[32:]
	cData += '"{}"\n'.format(ret)
	print(cData)
def prnStr(hexData):
	global trainingModeRdt
	trainingModeRdt = ''.join(chr(x) for x in hexData)
	print(trainingModeRdt)
	if trainingModeRdt.isprintable():
		print('isprintable')
def getData8File(inData):
	hexData = []
	try:
		for line in inData.split('\n'):
			items = line.split(' ')
			for item in items[1:9]:
				tmp = int(item, 16)
				hexData.append(tmp)
	except ValueError:
		hexData = srhDate(hexData)
		print(hexData,'\n')
		prnByte(hexData)
		prnStr(hexData)
		

print('111111111111111')
getData8File(inData1)
print('2222222222222222')
getData8File(inData2)
print('33333333333333333')
#############################################	
#trainingModeRdt = '02JUN18@@X@BHVB04JUN18@       @       AHA@`@@@@@~C@C@H@@TA@D@@C@S1A03JUN18@       @       DNxA@H@@@@KF@O~CB@@DB@@B@O~CRDT FOR TRAINING'
#trainingModeRdt =  '\x30\x38\x44\x45\x43\x31\x39\x40\x40\x7F\x41\x41\x53\x31\x43\x31\x30\x44\x45\x43\x31\x39\x40\x20\x20\x20\x20\x20\x20\x20\x40\x20\x20\x20\x20\x20\x20\x20\x41\x46\x5F\x40\x40\x48\x40\x40\x40\x40\x40\x7F\x40\x40\x7F\x40\x40\x44\x40\x40\x55\x40\x40\x41\x40\x40\x7F\x40\x40\x49\x24'
trkInfoNames = ['dbl','tbl','d_q','qtt','tce','t_t','d_t','six_up','fct']
trkNames = [['ST',0x41],['HV',0x42],['S1',0x45],['S2',0x46],['X1',0x43],['',0x44]
]

def findRecIn1col(table, keyInx, srhData):
	for record in table:
		if record[keyInx] == srhData:
			return record
	return []
def getDate():
	global tablePtr
	tmp = trainingModeRdt[tablePtr:tablePtr + 7]
	tablePtr+= 7
#	return datetime.strptime(tmp, '%d%b%y').date()
	return tmp
def getInt(sz):
	global tablePtr
	ret = 0
	for i in range(sz):
		ret+= (ord(trainingModeRdt[tablePtr]) & 0x3f) << (6 * i)
		tablePtr += 1
	return ret
def getString(sz):
	global tablePtr
	remain = len(trainingModeRdt) - tablePtr
	if remain < sz:
		sz = remain
	ret = trainingModeRdt[tablePtr:tablePtr + sz]
	tablePtr += sz
	return ret
def str2intstr(str):
	ret = ''
	for s in str:
		s = chr(ord(s) | 0x40)
		ret += s
	return ret	

def getReply():	
	global tablePtr
	tablePtr = 0

	m_currentDate	= getDate()		#m_rdt->current_day
	m_GBLDrawNumber	= getInt(2)		#m_rdt->draw_no
	m_MK6DrawNumber	= getInt(2)		#m_rdt->ball_no
	m_numberOfTracks= getInt(1)		#m_rdt->no_of_tracks
	print(m_currentDate)
	print(m_GBLDrawNumber)
	print(m_MK6DrawNumber)
	print(m_numberOfTracks)
	for i in range(m_numberOfTracks):
		trackName = getString(2)		#m_rdt->track[i].track
		record = findRecIn1col(trkNames, 0, trackName)
		print('----', trackName, chr(record[1]))
		raceDate = []
		for j in range(3):
			raceDayCode = getString(1)		#m_rdt->track[i].day[j]
			race_day = getDate()			#m_rdt->track[i].race_day[j]
			raceDate.append([raceDayCode, race_day])
			#print('--------',[raceDayCode, race_day])
		print('----', raceDate)
		firstRace= getInt(1)			#m_rdt->track[i].low_race
		lastRace = getInt(1)			#m_rdt->track[i].high_race
		print('----',firstRace,lastRace)
		TrackInfo= []
		for j in range(len(trkInfoNames)):
			tmp = getInt(3)
			tmp= '{0:b}'.format(tmp)	
			pool = tmp.zfill(18)			#m_rdt->track[i].dbl
			pool = pool[::-1]
			TrackInfo.append(pool)
			print('--------', pool, trkInfoNames[j])		
	broadcastMessage = getString(32)
	print(broadcastMessage)
getReply()
	

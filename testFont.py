import numpy as np
from PIL import Image, ImageDraw, ImageFont

def getUTF8size(ch):
	if ch < 0x80:
		return 1
	tmp = ch & 0xF0
	if tmp == 0xF0:
		return 4
	if tmp == 0xE0:
		return 3
	tmp = tmp & 0xC0
	if tmp == 0xC0:
		return 2
	return -1
def utf8toUnicode(strUTF8):
	bytes = strUTF8.encode('utf-8')
	return bytes.decode()
def unicode2utf8(str):
	bytes = str.encode()
	return bytes.decode('utf-8')
def chRange2fontInx(fontRanges, unicode):
	offset = 0
	for range in fontRanges:
		if unicode < range[0]:
			break
		if unicode <= range[1]:
			return unicode - range[0]
		offset += range[1] + 1 - range[0]
	return -1
def getFont(fontRanges, name, size, unicode_text):
	font = ImageFont.truetype(name, size, encoding="unic")
	text_width, text_height = font.getsize(unicode_text)
	canvas = Image.new('RGBA', (text_width, text_height), "black")
	draw = ImageDraw.Draw(canvas)
	draw.text((0, 0), unicode_text, 'white', font)
	bw = canvas.convert('1')
	aryRGB = np.array(canvas)
	aryBW = np.array(bw)
#	print (canvas.getpixel((1, 1)))
	print(aryRGB)
	print (bw.getpixel((1, 1)))
	print(aryBW)
	return text_width, text_height
''''
unicode_text = u"HMKXZW"
font = ImageFont.truetype("arial.ttf", 28, encoding="unic")
text_width, text_height = font.getsize(unicode_text)
canvas = Image.new('RGB', (text_width, text_height), "black")
draw = ImageDraw.Draw(canvas)
draw.text((0, 0), unicode_text, 'white', font)
canvas.save("unicode-text.png", "PNG")
bw = canvas.convert('1')
bw.save("bw.png", "PNG")
canvas.show()
'''
fontRanges = [
	[	0x20,	0x7f	]
]
getFont(fontRanges, "arial.ttf", 10, u"M")
	
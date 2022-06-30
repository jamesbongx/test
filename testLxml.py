#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import shutil
import codecs
import numpy as np
import copy
from lxml import etree
from io import BytesIO

#https://lxml.de/tutorial.html

root = etree.Element("root")
root.append( etree.Element("child1") )
child2 = etree.SubElement(root, "child2")
print(etree.tostring(root, pretty_print=True))
child = root[0]
print(child.tag)
children = list(root)
for child in root:
	print(child.tag)
root.insert(0, etree.Element("child0"))
start = root[:1]
end   = root[-1:]
print(start[0].tag)
etree.SubElement(root, "child").text = "Child 1"
etree.SubElement(root, "another").text = "Child 3"
print(etree.tostring(root, pretty_print=True))
for element in root.iter():
	print("%s - %s" % (element.tag, element.text))
print('??????1')
for element in root.iter("child"):	
	print("%s - %s" % (element.tag, element.text))
print('?????')
for element in root.iter("another", "child"):
	print("%s - %s" % (element.tag, element.text))
root.append(etree.Entity("#234"))
root.append(etree.Comment("some comment"))
print('?????2')
for element in root.iter():
	if isinstance(element.tag, str):
		print("%s - %s" % (element.tag, element.text))
	else:
		print("SPECIAL: %s - %s" % (element, element.text))
print('?????3')
for element in root.iter(tag=etree.Element):
	print("%s - %s" % (element.tag, element.text))		
print('?????4')
for element in root.iter(tag=etree.Entity):
	print(element.text)
print('?????5')
root = etree.XML('<root><a><b/></a></root>')
print(etree.tostring(root))
print(etree.tostring(root, xml_declaration=True))
print(etree.tostring(root, encoding='iso-8859-1'))
print(etree.tostring(root, pretty_print=True))
print('?????6')
root = etree.XML('<root><a><b/>\n</a></root>')
print(etree.tostring(root))
print('?????6-indent')
etree.indent(root)
print(etree.tostring(root))
print('?????6-text')
print(root.text)
print('?????6-text[0]')
print(root[0].text)
print('?????6-space')
etree.indent(root, space="    ")
print(etree.tostring(root))
print('?????6-tab')
etree.indent(root, space="\t")
print(etree.tostring(root))
print('?????7')
root = etree.XML('<html><head/><body><p>Hello<br/>World</p></body></html>')
print(etree.tostring(root))
print(etree.tostring(root, method='xml'))
print(etree.tostring(root, method='html'))
print(etree.tostring(root, method='html', pretty_print=True))
print(etree.tostring(root, method='text'))
br = next(root.iter('br'))
br.tail = u'W\xf6rld'
#print(etree.tostring(root, method='text'))
print(etree.tostring(root, method='text', encoding="UTF-8"))
print(etree.tostring(root, encoding='unicode', method='text'))
print('?????8')
root = etree.XML('''<?xml version="1.0"?>
<!DOCTYPE root SYSTEM "test" [ <!ENTITY tasty "parsnips"> ]>
<root>
	<a>&tasty;</a>
</root>
	''')
tree = etree.ElementTree(root)
tree.write('output.xml', pretty_print=True)
print(tree.docinfo.xml_version)
print(tree.docinfo.doctype)
print('?????8a')
tree.docinfo.public_id = '-//W3C//DTD XHTML 1.0 Transitional//EN'
tree.docinfo.system_url = 'file://local.dtd'
print(tree.docinfo.doctype)
print(etree.tostring(tree)) 
print('?????8b')
print(etree.tostring(tree.getroot()))
print('?????9')
some_xml_data = "<root>data</root>"
root = etree.fromstring(some_xml_data)
print(root.tag)
print(etree.tostring(root))
root = etree.XML("<root>data</root>")
print(etree.tostring(root))
root = etree.HTML("<p>data</p>")
print(etree.tostring(root))
print('?????10')
some_file_or_file_like_object = BytesIO(b"<root>data</root>")
tree = etree.parse(some_file_or_file_like_object)
print(etree.tostring(tree))
print('?????11')
parser = etree.XMLParser(remove_blank_text=True)
root = etree.XML("<root>  <a/>   <b>  </b>     </root>", parser)
print(etree.tostring(root))
for element in root.iter("*"):
	if element.text is not None and not element.text.strip():
		element.text = None
print(etree.tostring(root))
print('?????12')
class DataSource:
	data = [ b"<roo", b"t><", b"a/", b"><", b"/root>" ]
	def read(self, requested_size):
		try:
			return self.data.pop(0)
		except IndexError:
			return b''
tree = etree.parse(DataSource())
print(etree.tostring(tree))
print('?????13')
parser = etree.XMLParser()
parser.feed("<roo")
parser.feed("t><")
parser.feed("a/")
parser.feed("><")
parser.feed("/root>")
root = parser.close()
print(etree.tostring(root))
print('?????14')
some_file_like = BytesIO(b"<root><a>data</a></root>")
for event, element in etree.iterparse(some_file_like):
	print("???%s, %4s, %s" % (event, element.tag, element.text))
print('?????14a')
some_file_like = BytesIO(b"<root><a>data</a></root>")
for event, element in etree.iterparse(some_file_like,events=("start", "end")):
	print("???%5s, %4s, %s" % (event, element.tag, element.text))
print('?????14b')
some_file_like = BytesIO(b"<root><a><b>data</b></a><a><b/></a></root>")
for event, element in etree.iterparse(some_file_like):
	if element.tag == 'b':
		print(element.text)
	elif element.tag == 'a':
		print("** cleaning up the subtree")
		element.clear(keep_tail=True)
print('?????14c')
xml_file = BytesIO(b'''<root>
		<a><b>ABC</b><c>abc</c></a>
		<a><b>MORE DATA</b><c>more data</c></a>
		<a><b>XYZ</b><c>xyz</c></a>
	</root>''')
for _, element in etree.iterparse(xml_file, tag='a'):
	print('%s -- %s' % (element.findtext('b'), element[1].text))
	element.clear(keep_tail=True)
print('?????15')
class ParserTarget:
	events = []
	close_count = 0
	def start(self, tag, attrib):
		self.events.append(("start", tag, attrib))
	def close(self):
		events, self.events = self.events, []
		self.close_count += 1
		return events
parser_target = ParserTarget()
parser = etree.XMLParser(target=parser_target)
events = etree.fromstring('<root test="true"/>', parser)
print(parser_target.close_count)
for event in events:
	print('event: %s - tag: %s' % (event[0], event[1]))
	for attr, value in event[2].items():
		print(' * %s = %s' % (attr, value))	
print('?????16')
events = etree.fromstring('<root test="true"/>', parser)
print(parser_target.close_count)
events = etree.fromstring('<root test="true"/>', parser)
print(parser_target.close_count)
events = etree.fromstring('<root test="true"/>', parser)
print(parser_target.close_count)
for event in events:
	print('event: %s - tag: %s' % (event[0], event[1]))
	for attr, value in event[2].items():
		print(' * %s = %s' % (attr, value))
print('?????17')
xhtml = etree.Element("{http://www.w3.org/1999/xhtml}html")
body = etree.SubElement(xhtml, "{http://www.w3.org/1999/xhtml}body")
body.text = "Hello World"
print(etree.tostring(xhtml, pretty_print=True))
print('?????17')
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
XHTML = "{%s}" % XHTML_NAMESPACE
NSMAP = {None : XHTML_NAMESPACE} # the default namespace (no prefix)
xhtml = etree.Element(XHTML + "html", nsmap=NSMAP) # lxml only!
body = etree.SubElement(xhtml, XHTML + "body")
body.text = "Hello World"
print(etree.tostring(xhtml, pretty_print=True))
print('?????18')
tag = etree.QName('http://www.w3.org/1999/xhtml', 'html')
print(tag.localname)
print(tag.namespace)
print(tag.text)
tag = etree.QName('{http://www.w3.org/1999/xhtml}html')
print(tag.localname)
print(tag.namespace)
root = etree.Element('{http://www.w3.org/1999/xhtml}html')
tag = etree.QName(root)
print(tag.localname)
tag = etree.QName(root, 'script')
print(tag.text)
tag = etree.QName('{http://www.w3.org/1999/xhtml}html', 'script')
print(tag.text)
print('?????19')
root = etree.Element('root', nsmap={'a': 'http://a.b/c'})
child = etree.SubElement(root, 'child',nsmap={'b': 'http://b.c/d'})
print(len(root.nsmap))
print(len(child.nsmap))
print(child.nsmap['a'])
print(child.nsmap['b'])
print('?????20')
body.set(XHTML + "bgcolor", "#CCFFAA")
print(etree.tostring(xhtml, pretty_print=True))
print(body.get("bgcolor"))
print('?????21')
find_xhtml_body = etree.ETXPath("//{%s}body" % XHTML_NAMESPACE)
results = find_xhtml_body(xhtml)
print(results[0].tag)
print('?????21a')
for el in xhtml.iter('*'): print(el.tag)
for el in xhtml.iter('{http://www.w3.org/1999/xhtml}*'): print(el.tag)
for el in xhtml.iter('{*}body'): print(el.tag)
print('?????21b')
print([ el.tag for el in xhtml.iter('{http://www.w3.org/1999/xhtml}body') ])
print([ el.tag for el in xhtml.iter('body') ])
print([ el.tag for el in xhtml.iter('{}body') ])
print([ el.tag for el in xhtml.iter('{}*') ])
print('?????22')
root = etree.XML("<root><a x='123'>aText<b/><c/><b/></a></root>")
print(root.find("b"))
print(root.find("a").tag)
print(root.find(".//b").tag)
print([ b.tag for b in root.iterfind(".//b") ])
print(root.findall(".//a[@x]")[0].tag)
print(root.findall(".//a[@y]"))
print('?????22a')
tree = etree.ElementTree(root)
a = root[0]
print(tree.getelementpath(a[0]))
print(tree.getelementpath(a[1]))
print(tree.getelementpath(a[2]))
print(tree.find(tree.getelementpath(a[2])) == a[2])
print(root.find(".//b").tag)
print(next(root.iterfind(".//b")).tag)
print(next(root.iter("b")).tag)

print('??????????????????????????')
with open('example.xml') as fobj:
	xml = fobj.read()
root = etree.fromstring(xml)
book_dict = {}
books = []
for book in root.getchildren():
	for elem in book.getchildren():
		if not elem.text:
			text = "None"
		else:
			text = elem.text
			print(elem.tag + " => " + text)
			book_dict[elem.tag] = text
		if book.tag == "book":
			books.append(book_dict)
			book_dict = {}
print('****')
print(books)
print('??????????????????????????')
for country in root.findall('book'):
    genre = country.find('genre').text
    print(genre)
	
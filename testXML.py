#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import shutil
import codecs
import numpy as np
import copy
import xml.etree.ElementTree as ET

#https://docs.python.org/3/library/xml.etree.elementtree.html

tree = ET.parse('country_data.xml')
root = tree.getroot()
#root = ET.fromstring(country_data_as_string)
print(root.tag)
print(root.attrib)
for child in root:
	print(child.tag, child.attrib)
print(root[0][1].text)
print('???????1')
parser = ET.XMLPullParser(['start', 'end'])
parser.feed('<mytag>sometext')
print(list(parser.read_events()))
parser.feed(' more text</mytag>')
print('???????1a')
for event, elem in parser.read_events():
	print(event)
	print(elem.tag, 'text=', elem.text)
print('???????1b')
for neighbor in root.iter('neighbor'):
	print(neighbor.attrib)	
print('???????1c')
for country in root.findall('country'):
	rank = country.find('rank').text
	name = country.get('name')
	print(name, rank, type(country), type(rank))	

for rank in root.iter('rank'):
	new_rank = int(rank.text) + 1
	rank.text = str(new_rank)
	rank.set('updated', 'yes')
tree.write('output.xml')

for country in root.findall('country'):
# using root.findall() to avoid removal during traversal
	rank = int(country.find('rank').text)
	if rank > 50:
		root.remove(country)
tree.write('output1.xml')
print('???????1d')
print(root.findall("."))
# All 'neighbor' grand-children of 'country' children of the top-level elements
print(root.findall("./country/neighbor"))
# Nodes with name='Singapore' that have a 'year' child
print(root.findall(".//year/..[@name='Singapore']"))
# 'year' nodes that are children of nodes with name='Singapore'
print(root.findall(".//*[@name='Singapore']/year"))
# All 'neighbor' nodes that are the second child of their parent
print(root.findall(".//neighbor[2]"))

a = ET.Element('a')
b = ET.SubElement(a, 'b')
c = ET.SubElement(a, 'c')
d = ET.SubElement(c, 'd')
ET.dump(a)

xml_text = '''<?xml version="1.0"?>
<actors xmlns:fictional="http://characters.example.com"
        xmlns="http://people.example.com">
    <actor>
        <name>John Cleese</name>
        <fictional:character>Lancelot</fictional:character>
        <fictional:character>Archie Leach</fictional:character>
    </actor>
    <actor>
        <name>Eric Idle</name>
        <fictional:character>Sir Robin</fictional:character>
        <fictional:character>Gunther</fictional:character>
        <fictional:character>Commander Clement</fictional:character>
    </actor>
</actors>
	'''
root = ET.fromstring(xml_text)
for actor in root.findall('{http://people.example.com}actor'):
	name = actor.find('{http://people.example.com}name')
	print(name.text)
	for char in actor.findall('{http://characters.example.com}character'):
		print(' |-->', char.text)
print('???????2a')
ns={'real_person': 'http://people.example.com',
	'role': 'http://characters.example.com'}
for actor in root.findall('real_person:actor', ns):
	name = actor.find('real_person:name', ns)
	print(name.text)
	for char in actor.findall('role:character', ns):
		print(' |-->', char.text)

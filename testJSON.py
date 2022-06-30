import json
from pprint import pprint

x =  '{ "name":"John", "age":30, "city":"New York"}'
y = json.loads(x)
print(y)
pprint(y)
print(type(y))
print(y["age"])
print('1111111111')
x = json.dumps(y, indent=4, sort_keys=True)
print(x)
print(type(x))
print('2222222222')
with open('orders.json') as file:
	data = json.load(file)
	print(data)
	print(len(data))
	print(data["orders"])
	print(len(data["orders"]))
	for order in data["orders"]:
		del order["client"]
print('3333333333')
with open("orders_new.json", 'w') as file:
	json.dump(data, file, indent=4, sort_keys=True)
print('4444444444')
f = open('orders.json')
data = json.load(f)
print(data)
f.close()
print('5555555555')
f = open('orders.json')
data = json.loads(f.read())
print(data)
f.close()
print('6666666666')
courses={
	'seq': [
		{
			"betslip": "slip.bin",
			"reply": "reply.txt",
			"xml": [	
				"F20210422_180459671_1333_1_7_FBTournament.xml",	
			]
		},
		{
			"betslip": "slip.1bin",
			"reply": "reply1.txt",
			"xml": [	
				"F20210422_180459671_1333_1_7_FBTournament.xml",	
			]
		}
	]
}

print(courses)
x = json.dumps(courses, indent=4, sort_keys=True)
print(x)

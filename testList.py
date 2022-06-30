#https://note.nkmk.me/en/python-slice-usage/

l = ['Alice', 'Bob', 'Charlie', 'Bob', 'Dave']

print([s for s in l if s != 'Bob'])
print([s for s in l if s.endswith('e')])
print(list(set(l)))

l.remove('Alice')
print(l)

l = list(range(10))

print(l[2:5])
print(l[5:2:-1])
print(l[-2:-5:-1])
print([i for i in l if i % 2 == 0])

del l[6]
#del l[-1]
#del l[2:5]
#del l[:3]
#del l[4:]
#del l[-3:]
#del l[:]
#del l[2:8:2]
#del l[::3]
print(l)

#print(l.pop(3))
#print(l.pop(-2))
#print(l.pop())
#print(l)

#l.clear()
#print(l)

names = ['Alice', 'Bob', 'Charlie']
ages = [24, 50, 18]
for name, age in zip(names, ages):
    print(name, age)
	
names = ['Alice', 'Bob', 'Charlie', 'Dave']
ages = [24, 50, 18]
for name, age in zip(names, ages):
    print(name, age)

from operator import itemgetter, attrgetter

student_tuples = [
    ['john', 'A', '19'],
    ['jane', 'E', '12'],
    ['dav1', 'K', '15'],
    ['dav5', 'F', '15'],
    ['dav3', 'B', '15'],
	]                 
print(student_tuples)
print(sorted(student_tuples, key=lambda student: student[2]))
print(sorted(student_tuples, key=itemgetter(2)))
print(sorted(student_tuples, key=itemgetter(2,1)))
print(sorted(student_tuples, key=itemgetter(2), reverse=True))
print(sorted(student_tuples, key=lambda student: (student[2], student[1])))
#https://stackabuse.com/padding-strings-in-python/
print('hi'.ljust(10))
print('hi'.rjust(10))
print('hi'.ljust(10,'.'))
print('hi'.rjust(10,'.'))
print('hi'.center(10,'.'))
print('{:^10}'.format('hi'))
print('{:>10}'.format('hi')) 
print('{:<10}'.format('hi')) 
print('{:.<10}'.format('hi')) 
print('hi'.zfill(10))
print('{:>010d}'.format(12))
student_tuples = [
    ['john', 'A', 9],
    ['jane', 'E', 2],
    ['dav3', 'a', 15],
    ['dav1' , 'x', 15],
    ['dav1a', 'c', 15],
	]                 
def getSortKey(elem):
	ret = ''
	for i in sortKeyLst:
		if type(i) == list:
			ret += elem[i[0]].ljust(i[1])
		elif type(elem[i]) == int:
			ret += '{:>08d}'.format(elem[i])
		else:
			ret += elem[i]
	return ret
def sortList(orgLst, keyLst):
	global sortKeyLst
	sortKeyLst = keyLst
	return sorted(student_tuples, key=getSortKey)
print(sortList(student_tuples, [2, 0, 1]))
print(sortList(student_tuples, [2, [0,10], 1]))

print('!!!!!!!!!!!!!')
#https://www.programcreek.com/python/example/102034/functools.cmp_to_key
print(1>2)
print(['jane1', 'F', '13']>['jane2', 'E', '12'])
print('dav1a' > 'dav1')
import functools

def myCmp(x, y):
	for i in sortKeyLst:
		if x[i] != y[i]: 
			return 1 if x[i] > y[i] else -1
	return 0
def sortList1(orgLst, keyLst):
	global sortKeyLst
	sortKeyLst = keyLst
	return sorted(student_tuples, key=functools.cmp_to_key(myCmp))
print(sortList1(student_tuples, [0, 1, 2]))
print(sortList1(student_tuples, [2, 0, 1]))
print('CHP3'.replace('CHP', ''))
print('C HP3'.replace('CHP', ''))

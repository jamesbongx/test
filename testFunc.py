#https://www.adamsmith.haus/python/answers/how-to-pass-a-function-in-another-function-in-python
def repeat(function, n):
	return function(n)
def square(n):
	return n ** 2
output = repeat(square, 3)
print(output)
#https://www.danielmorell.com/blog/dynamically-calling-functions-in-python-safely
def area(length: int, width: int):
    print(length * width)
area_func = globals()["area"]
area_func(5, 5)
#https://www.adamsmith.haus/python/answers/how-to-call-a-function-by-its-name-as-a-string-in-python
def f():
	return "result"
result = eval("f()")
print(result)

class C:
	def m(self):
		return "resultC"
an_object = C()
class_method = getattr(C, "m")
result = class_method(an_object)
print(result)

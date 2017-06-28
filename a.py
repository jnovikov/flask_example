import requests


url = 'http://brute.shadowservants.ru/send.php'

data = {'login':'admin','pass':'12345'}

r = requests.get(url,params=data)

print(r.text)
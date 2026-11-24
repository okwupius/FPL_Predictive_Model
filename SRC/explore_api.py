import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

data = requests.get(url).json()

print(data.keys())

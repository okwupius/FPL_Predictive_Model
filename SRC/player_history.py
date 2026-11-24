import requests
import pandas as pd

player_id = 494

url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

data = requests.get(url).json()

history = pd.DataFrame(data["history"])

print("\nColumns Available:\n")
print(history.columns.tolist())
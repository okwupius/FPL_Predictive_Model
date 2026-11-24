import requests
import pandas as pd

url = "https://fantasy.premierleague.com/api/fixtures/"

fixtures = requests.get(url).json()

df = pd.DataFrame(fixtures)

print(df.columns.tolist())

df.to_csv(
    "data/processed/fixtures.csv",
    index=False
)

print(df.head())
import requests
import pandas as pd

player_id = 494

url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"

data = requests.get(url).json()

df = pd.DataFrame(data["history"])

# Rolling averages

df["avg_points_last_3"] = (
    df["total_points"]
    .shift(1)
    .rolling(3)
    .mean()
)

df["avg_points_last_5"] = (
    df["total_points"]
    .shift(1)
    .rolling(5)
    .mean()
)

df["avg_minutes_last_5"] = (
    df["minutes"]
    .shift(1)
    .rolling(5)
    .mean()
)

print(
    df[
        [
            "round",
            "total_points",
            "avg_points_last_3",
            "avg_points_last_5",
            "avg_minutes_last_5"
        ]
    ].tail(10)
)
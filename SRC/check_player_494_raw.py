# src/check_player_494_raw.py

import pandas as pd

df = pd.read_csv(
    "data/processed/all_player_history.csv"
)

player = df[df["player_id"] == 494]

print(player.head(20))

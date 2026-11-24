# src/check_player_columns.py

import pandas as pd

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

print(players.columns.tolist())
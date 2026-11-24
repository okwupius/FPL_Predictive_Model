# src/check_raw_player_file.py

import pandas as pd

players = pd.read_csv(
    "data/Raw/fpl_players.csv"
)

print(players.columns.tolist())

print(
    players[
        players["Last_Name"] == "Haaland"
    ]
)
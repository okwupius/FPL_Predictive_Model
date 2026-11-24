# src/check_haaland_mapping.py

import pandas as pd

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

print(
    mapping[
        mapping["Last_Name"] == "Haaland"
    ]
)

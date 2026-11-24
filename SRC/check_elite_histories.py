# src/check_elite_histories.py

import pandas as pd

hist = pd.read_csv(
    "data/processed/all_player_history.csv"
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

merged = hist.merge(
    mapping,
    on="player_id",
    how="left"
)

elite = merged[
    merged["Last_Name"].isin(
        ["Haaland", "Saka", "Isak", "Palmer"]
    )
]

print(
    elite.groupby(
        ["First_Name", "Last_Name"]
    )[
        ["minutes", "total_points"]
    ]
    .sum()
)

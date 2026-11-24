# src/check_history_quality.py

import pandas as pd

df = pd.read_csv(
    "data/processed/all_player_history.csv"
)

summary = (
    df.groupby("player_id")
      .agg(
          matches=("minutes", "count"),
          total_minutes=("minutes", "sum"),
          total_points=("total_points", "sum")
      )
)

print(
    summary.sort_values(
        "total_minutes",
        ascending=False
    ).head(20)
)

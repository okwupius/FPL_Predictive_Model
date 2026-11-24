import pandas as pd

df = pd.read_csv(
    "data/processed/v8_predictions.csv"
)

print(
    df.sort_values(
        "Projected_Points",
        ascending=True
    )[
        [
            "player_id",
            "Projected_Points",
            "avg_points_last_3",
            "avg_points_last_5",
            "avg_minutes_last_5",
            "Ownership",
            "xG",
            "xA"
        ]
    ].head(20)
)
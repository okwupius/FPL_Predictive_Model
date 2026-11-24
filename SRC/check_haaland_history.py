import pandas as pd

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

player = df[df["player_id"] == 494]

print(
    player[
        [
            "round",
            "minutes",
            "total_points",
            "avg_points_last_3",
            "avg_points_last_5"
        ]
    ]
    .tail(10)
)

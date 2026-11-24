import pandas as pd

df = pd.read_csv(
    "data/processed/all_player_history.csv"
)

player = df[
    df["player_id"] == 411
]

print(
    player[
        [
            "round",
            "minutes",
            "total_points",
            "goals_scored"
        ]
    ].tail(20)
)

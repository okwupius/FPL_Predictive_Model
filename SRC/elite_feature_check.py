import pandas as pd

forecast = pd.read_csv(
    "data/processed/forecast_dataset.csv"
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

df = forecast.merge(
    mapping,
    on="player_id",
    how="left"
)

elite = df[
    df["Last_Name"].isin(
        ["Haaland", "Saka", "Isak", "Palmer"]
    )
]

print(
    elite[
        [
            "First_Name",
            "Last_Name",
            "avg_points_last_3",
            "avg_points_last_5",
            "avg_minutes_last_5",
            "avg_goals_last_5",
            "avg_assists_last_5",
            "Ownership",
            "xG",
            "xA"
        ]
    ]
)

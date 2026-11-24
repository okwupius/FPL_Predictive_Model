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
    (
        (df["Last_Name"] == "Haaland")
        |
        (df["Last_Name"] == "Saka")
        |
        (df["Last_Name"] == "Isak")
        |
        (
            (df["First_Name"] == "Cole")
            &
            (df["Last_Name"] == "Palmer")
        )
    )
]

print(
    elite[
        [
            "First_Name",
            "Last_Name",
            "Price_x",
            "Ownership",
            "avg_points_last_3",
            "avg_points_last_5",
            "avg_minutes_last_5",
            "avg_goals_last_5",
            "avg_assists_last_5",
            "avg_bonus_last_5",
            "xG",
            "xA",
            "Attack_Strength",
            "Defence_Strength"
        ]
    ]
)
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

pd.set_option("display.max_columns", None)

print(elite)
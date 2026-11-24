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

print(df.columns.tolist())
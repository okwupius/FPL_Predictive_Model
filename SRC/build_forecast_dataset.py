import pandas as pd

# Load historical player data

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

# Sort by player and round

df = df.sort_values(
    ["player_id", "round"]
)

# Keep latest row for each player

forecast = (
    df.groupby("player_id")
      .tail(1)
      .copy()
)

# Remove target variable
# We are forecasting future points

forecast = forecast.drop(
    columns=["total_points"],
    errors="ignore"
)

# Save

forecast.to_csv(
    "data/processed/forecast_dataset.csv",
    index=False
)

print("Forecast Dataset Created")
print(forecast.shape)

print(
    forecast[
        [
            "player_id",
            "avg_points_last_3",
            "avg_points_last_5",
            "avg_minutes_last_5"
        ]
    ].head()
)
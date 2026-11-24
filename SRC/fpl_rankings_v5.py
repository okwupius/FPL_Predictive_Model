import pandas as pd

from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv(
    "data/processed/model_v5_data.csv"
)

features = [
    "avg_points_last_3",
    "avg_points_last_5",
    "avg_minutes_last_5",
    "avg_goals_last_5",
    "avg_assists_last_5",
    "avg_bonus_last_5",
    "home_game",
    "Price",
    "Ownership",
    "xG",
    "xA"
]

X = df[features]
y = df["total_points"]

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(X, y)

df["Predicted_Points"] = model.predict(X)

latest = (
    df.sort_values("round")
      .groupby("player_id")
      .tail(1)
)

mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

results = latest.merge(
    mapping,
    on="player_id",
    how="left"
)

results = results.sort_values(
    "Predicted_Points",
    ascending=False
)

print(
    results[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Predicted_Points"
        ]
    ].head(20)
)
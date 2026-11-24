import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load training data
df = pd.read_csv(
    "data/processed/training_data.csv"
)

features = [
    "avg_points_last_3",
    "avg_points_last_5",
    "avg_minutes_last_5"
]

X = df[features]

y = df["total_points"]

# Train model
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X, y)

# Predict
df["Predicted_Points"] = model.predict(X)

# Latest row for each player
latest = (
    df.sort_values("round")
      .groupby("player_id")
      .tail(1)
)

# Load player names
mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

# Merge names
results = latest.merge(
    mapping,
    on="player_id",
    how="left"
)

results = results.sort_values(
    "Predicted_Points",
    ascending=False
)

print("\nTOP 25 PROJECTED PLAYERS\n")

print(
    results[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Predicted_Points"
        ]
    ].head(25)
)
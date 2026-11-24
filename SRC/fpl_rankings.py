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

# Most recent record for each player
latest = (
    df.sort_values("round")
      .groupby("player_id")
      .tail(1)
)

# Load mapping
mapping = pd.read_csv(
    "data/processed/player_mapping.csv"
)

# Merge
results = latest.merge(
    mapping,
    on="player_id",
    how="left"
)

results = results.sort_values(
    "Predicted_Points",
    ascending=False
)
results.to_csv(
    "data/processed/latest_predictions.csv",
    index=False
)

print("\nTOP 20 PROJECTED PLAYERS\n")

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
print("\nBEST BUDGET PICKS (<6.0)\n")

budget = results[
    results["Price"] <= 6.0
]

print(
    budget[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Predicted_Points"
        ]
    ]
    .sort_values(
        "Predicted_Points",
        ascending=False
    )
    .head(10)
)
# Position Rankings

positions = {
    1: "Goalkeepers",
    2: "Defenders",
    3: "Midfielders",
    4: "Forwards"
}

for pos_id, pos_name in positions.items():

    print(f"\nTOP {pos_name.upper()}\n")

    filtered = results[
        results["Position"] == pos_id
    ]

    print(
        filtered[
            [
                "First_Name",
                "Last_Name",
                "Price",
                "Predicted_Points"
            ]
        ].head(10)
    )
    # Captain Picks
print("\nBEST CAPTAIN PICKS\n")

print(
    results[
        [
            "First_Name",
            "Last_Name",
            "Predicted_Points"
        ]
    ].head(5)
)

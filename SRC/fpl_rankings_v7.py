import pandas as pd

from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
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
    "xA",
    "Attack_Strength",
    "Defence_Strength"
]

X = df[features]
y = df["total_points"]

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(X, y)

df["Predicted_Points"] = model.predict(X)

print("\nMODEL DIAGNOSTICS\n")

print(
    df[
        [
            "total_points",
            "Predicted_Points"
        ]
    ].head(20)
)
print("\nTOP TRAINING ROWS\n")

print(
    df.sort_values(
        "Predicted_Points",
        ascending=False
    )[
        [
            "player_id",
            "total_points",
            "Predicted_Points",
            "avg_points_last_3",
            "avg_minutes_last_5"
        ]
    ].head(20)
)
df = df[
    df["avg_minutes_last_5"] >= 60
]

df = df[
    df["Ownership"] >= 1
]
df = df[
    df["Price"] >= 5.0
]
df = df[
    df["avg_minutes_last_5"] >= 75
]

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

# Clean up duplicate column names after merge

results = results.rename(
    columns={
        "Price_x": "Price",
        "Position_x": "Position",
        "Team_x": "Team"
    }
)
results = results.drop(
    columns=[
        "Price_y",
        "Position_y",
        "Team_y"
    ]
)

results.to_csv(
    "data/processed/latest_predictions_v7.csv",
    index=False
)

print(results.columns.tolist())

results = results.sort_values(
    "Predicted_Points",
    ascending=False
)

print("\nTOP EXPENSIVE PLAYERS\n")

expensive = results[
    results["Price"] >= 8.0
]

print(
    expensive[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Ownership",
            "Predicted_Points"
        ]
    ].head(20)
)

print("\nBOTTOM 20 PLAYERS\n")

print(
    results[
        [
            "First_Name",
            "Last_Name",
            "Price",
            "Predicted_Points"
        ]
    ]
    .tail(20)
)

results["Rank"] = range(
    1,
    len(results) + 1
)
elite = results[
    (
        (results["Last_Name"] == "Haaland")
        |
        (results["Last_Name"] == "Saka")
        |
        (results["Last_Name"] == "Isak")
        |
        (
            (results["First_Name"] == "Cole")
            &
            (results["Last_Name"] == "Palmer")
        )
    )
]

print("\nELITE PLAYER CHECK\n")

print(
    elite[
        [
            "Rank",
            "First_Name",
            "Last_Name",
            "Price",
            "Ownership",
            "xG",
            "xA",
            "Predicted_Points"
        ]
    ]
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
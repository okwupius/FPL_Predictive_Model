import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# ------------------
# TRAINING DATA
# ------------------

df = pd.read_csv(
    "data/processed/model_v7_data.csv"
)

# Add fixture features used during training

df["Fixture_Difficulty"] = df["opponent_team"].map(
    lambda x: 3
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
    "Defence_Strength",
    "Fixture_Difficulty"
]

X = df[features]
y = df["total_points"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

preds = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    preds
)

print(f"\nV9 MAE: {mae:.2f}")

print("\nFEATURE IMPORTANCE\n")

importance = pd.DataFrame(
    {
        "Feature": features,
        "Importance": model.feature_importances_
    }
)

print(
    importance.sort_values(
        "Importance",
        ascending=False
    )
)

# ------------------
# FORECAST DATA
# ------------------

forecast = pd.read_csv(
    "data/processed/forecast_dataset_v9.csv"
)

X_forecast = forecast[features]

forecast["Projected_Points"] = model.predict(
    X_forecast
)

forecast.to_csv(
    "data/processed/v9_predictions.csv",
    index=False
)

print("\nTOP PROJECTED PLAYERS\n")

print(
    forecast[
        [
            "player_id",
            "Projected_Points"
        ]
    ]
    .sort_values(
        "Projected_Points",
        ascending=False
    )
    .head(20)
)
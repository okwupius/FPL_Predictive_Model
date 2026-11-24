import pandas as pd

from sklearn.ensemble import RandomForestRegressor

# --------------------------
# TRAIN V11 MODEL
# --------------------------

train = pd.read_csv(
    "data/processed/model_v11_data.csv"
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
    "Opponent_Attack_Strength",
    "Opponent_Defence_Strength",
    "Total_Points",
    "Form"
]

X_train = train[features]
y_train = train["total_points"]

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# --------------------------
# FORECAST V11
# --------------------------

forecast = pd.read_csv(
    "data/processed/forecast_v11.csv"
)

X_forecast = forecast[features]

forecast["Projected_Points"] = model.predict(
    X_forecast
)

forecast.to_csv(
    "data/processed/v11_predictions.csv",
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
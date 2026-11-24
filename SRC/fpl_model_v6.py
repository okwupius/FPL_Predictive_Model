import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

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

# Sort by gameweek

df = df.sort_values("round")

# Train on early gameweeks
train = df[df["round"] <= 7]

# Test on later gameweeks
test = df[df["round"] > 7]

X_train = train[features]
y_train = train["total_points"]

X_test = test[features]
y_test = test["total_points"]

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"\nTime-Series MAE: {mae:.2f}")

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE\n")

print(importance)
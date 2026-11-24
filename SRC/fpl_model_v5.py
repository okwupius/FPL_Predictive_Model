import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load merged dataset

df = pd.read_csv(
    "data/processed/model_v5_data.csv"
)

# Features

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

# Inputs and target

X = df[features]

y = df["total_points"]

# Train/Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model

model = RandomForestRegressor(
    n_estimators=500,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions

predictions = model.predict(X_test)

# Accuracy

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"\nModel V5 MAE: {mae:.2f}")

# Feature Importance

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

# Generate predictions for all rows

df["Predicted_Points"] = model.predict(X)

# Save predictions

df.to_csv(
    "data/processed/model_v5_predictions.csv",
    index=False
)

print(
    "\nPredictions saved to "
    "data/processed/model_v5_predictions.csv"
)